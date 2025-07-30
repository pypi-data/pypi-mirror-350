#![warn(clippy::all)]
use async_trait::async_trait;
use bytes::BytesMut;
use credentials::signer::{self, resign_streaming_request, signature_is_valid_for_presigned, signature_is_valid_for_request};
use dotenv::dotenv;
use http::Uri;
use http::uri::Authority;
use parsers::cos_map::{CosMapItem, parse_cos_map};
use parsers::keystore::parse_hmac_list;
use pingora::http::ResponseHeader;
use pingora::Result;
use pingora::proxy::{ProxyHttp, Session};
use pingora::server::Server;
use pingora::upstreams::peer::HttpPeer;
use pyo3::prelude::*;
use pyo3::types::{PyModule, PyModuleMethods};
use pyo3::{Bound, PyResult, Python, pyclass, pyfunction, pymodule, wrap_pyfunction};
use std::sync::{
    Arc,
    atomic::{AtomicBool, AtomicUsize, Ordering},
};

// use utils::functions::inspect_callable_signature;


use std::collections::HashMap;
use std::fmt::Debug;

use std::time::Duration;
use tokio::sync::RwLock;
use tracing::{debug, error, info};
use tracing_subscriber::EnvFilter;
use tracing_subscriber::fmt::time::ChronoLocal;


pub mod parsers;
use parsers::credentials::{parse_presigned_params, parse_token_from_header};
use parsers::path::{parse_path, parse_query};

pub mod credentials;
use credentials::{
    secrets_proxy::{SecretsCache, get_bearer, get_credential_for_bucket},
    signer::sign_request
};

pub mod utils;
use utils::validator::{AuthCache, validate_request};


static REQ_COUNTER: AtomicUsize = AtomicUsize::new(0);
static REQ_COUNTER_ENABLED: AtomicBool = AtomicBool::new(false);

/// Configuration object for :pyfunc:`object_storage_proxy.start_server`.
///
/// Parameters
/// ----------
/// cos_map:
///    A dictionary mapping bucket names to their respective COS configuration.
///   Each entry should contain the following
///   keys:
///   - host: The COS endpoint (e.g., "s3.eu-de.cloud-object-storage.appdomain.cloud")
///   - port: The port number (e.g., 443)
///   - api_key/apikey: The API key for the bucket (optional)
///   - ttl/time-to-live: The time-to-live for the API key in seconds (optional)
///
/// bucket_creds_fetcher:
///     Optional Python async callable that fetches the API key for a bucket.
///     The callable should accept a single argument, the bucket name.
///     It should return a string containing the API key.
/// http_port:
///     The HTTP port to listen on.
/// https_port:
///     The HTTPS port to listen on.
/// validator:
///     Optional Python async callable that validates the request.
///     The callable should accept two arguments, the token and the bucket name.
///     It should return a boolean indicating whether the request is valid.
/// threads:
///     Optional number of threads to use for the server.
///     If not specified, the server will use a single thread.
///
#[pyclass]
#[pyo3(name = "ProxyServerConfig")]
#[derive(Debug)]
pub struct ProxyServerConfig {
    #[pyo3(get, set)]
    pub bucket_creds_fetcher: Option<Py<PyAny>>,

    #[pyo3(get, set)]
    pub cos_map: PyObject,

    #[pyo3(get, set)]
    pub http_port: Option<u16>,

    #[pyo3(get, set)]
    pub https_port: Option<u16>,

    #[pyo3(get, set)]
    pub validator: Option<Py<PyAny>>,

    #[pyo3(get, set)]
    pub threads: Option<usize>,

    #[pyo3(get, set)]
    pub verify: Option<bool>,

    #[pyo3(get, set)]
    pub hmac_keystore: PyObject,

    #[pyo3(get, set)]
    pub skip_signature_validation: Option<bool>,

   #[pyo3(get, set)]
   pub hmac_fetcher: Option<Py<PyAny>>
}

impl Default for ProxyServerConfig {
    fn default() -> Self {
        ProxyServerConfig {
            cos_map: Python::with_gil(|py| py.None()),
            bucket_creds_fetcher: None,
            http_port: None,
            https_port: None,
            validator: None,
            threads: Some(1),
            verify: None,
            hmac_keystore: Python::with_gil(|py| py.None()),
            skip_signature_validation: Some(false),
            hmac_fetcher: None,
        }
    }
}

#[pymethods]
impl ProxyServerConfig {
    #[new]
    #[pyo3(
        signature = (
            cos_map,
            hmac_keystore = None,
            bucket_creds_fetcher = None,
            http_port = None,
            https_port = None,
            validator = None,
            threads = Some(1),
            verify = None,
            skip_signature_validation = Some(false),
            hmac_fetcher = None,
        )
    )]
    pub fn new(
        cos_map: PyObject,
        hmac_keystore: Option<PyObject>,
        bucket_creds_fetcher: Option<PyObject>,
        http_port: Option<u16>,
        https_port: Option<u16>,
        validator: Option<PyObject>,
        threads: Option<usize>,
        verify: Option<bool>,
        skip_signature_validation: Option<bool>,
        hmac_fetcher: Option<PyObject>,
    ) -> Self {
        ProxyServerConfig {
            cos_map,
            hmac_keystore: hmac_keystore.unwrap_or_else(|| Python::with_gil(|py| py.None())),
            bucket_creds_fetcher,
            http_port,
            https_port,
            validator,
            threads,
            verify,
            skip_signature_validation,
            hmac_fetcher,
        }
    }

    fn __repr__(&self) -> PyResult<String> {
        Ok(format!(
            "ProxyServerConfig(http_port={}, https_port={}, threads={:?})",
            self.http_port.unwrap_or(0), self.https_port.unwrap_or(0), self.threads
        ))
    }
}

pub struct MyProxy {
    cos_endpoint: String,
    cos_mapping: Arc<RwLock<HashMap<String, CosMapItem>>>,
    hmac_keystore: Arc<RwLock<HashMap<String, String>>>,
    secrets_cache: SecretsCache,
    auth_cache: AuthCache,
    validator: Option<PyObject>,
    bucket_creds_fetcher: Option<PyObject>,
    verify: Option<bool>,
    skip_signature_validation: Option<bool>,
    hmac_fetcher: Option<PyObject>,

}

pub struct MyCtx {
    cos_mapping: Arc<RwLock<HashMap<String, CosMapItem>>>,
    hmac_keystore: Arc<RwLock<HashMap<String, String>>>,
    secrets_cache: SecretsCache,
    auth_cache: AuthCache,
    validator: Option<PyObject>,
    bucket_creds_fetcher: Option<PyObject>,
    hmac_fetcher: Option<PyObject>,
    is_presigned: Option<bool>,
    stream_state: Option<signer::StreamingState>,
    
}

// impl MyCtx {
//     fn streaming(&mut self) -> &mut signer::StreamingState {
//         self.stream_state.as_mut().expect("stream_state not initialised")
//     }
// }

#[async_trait]
impl ProxyHttp for MyProxy {
    type CTX = MyCtx;
    fn new_ctx(&self) -> Self::CTX {
        MyCtx {
            cos_mapping: Arc::clone(&self.cos_mapping),
            hmac_keystore: Arc::clone(&self.hmac_keystore),
            secrets_cache: self.secrets_cache.clone(),
            auth_cache: self.auth_cache.clone(),
            validator: self
                .validator
                .as_ref()
                .map(|v| Python::with_gil(|py| v.clone_ref(py))),
            bucket_creds_fetcher: self
                .bucket_creds_fetcher
                .as_ref()
                .map(|v| Python::with_gil(|py| v.clone_ref(py))),
            hmac_fetcher: self
                .hmac_fetcher
                .as_ref()
                .map(|v| Python::with_gil(|py| v.clone_ref(py))),
            is_presigned: None,
            stream_state: None,
        }
    }

    async fn upstream_peer(
        &self,
        session: &mut Session,
        ctx: &mut Self::CTX,
    ) -> Result<Box<HttpPeer>> {
        debug!("upstream_peer::start");
        if REQ_COUNTER_ENABLED.load(Ordering::Relaxed) {
            let new_val = REQ_COUNTER.fetch_add(1, Ordering::Relaxed) + 1;
            debug!("Request count: {}", new_val);
        }

        let path = session.req_header().uri.path();


        let parse_path_result = parse_path(path);
        if parse_path_result.is_err() {
            error!("Failed to parse path: {:?}", parse_path_result);
            return Err(pingora::Error::new_str("Failed to parse path"));
        }

        let (_, (bucket, _)) = parse_path_result.unwrap();

        let hdr_bucket = bucket.to_owned();

        let bucket_config = {
            let map = ctx.cos_mapping.read().await;
            map.get(&hdr_bucket).cloned()
        };

        let addressing_style = bucket_config.clone()
            .and_then(|config| config.addressing_style)
            .unwrap_or("virtual".to_string());

        let endpoint = match bucket_config.clone() {
            Some(config) => {
                if addressing_style == "path" {
                    config.host.to_owned()
                } else {
                    format!("{}.{}", bucket, config.host)
                }            
            },
            None => {
                format!("{}.{}", bucket, self.cos_endpoint)
            }
        };

        let port = bucket_config.clone()
            .and_then(|config| Some(config.port))
            .unwrap_or(443);

        let addr = (endpoint.clone(), port);

        let endpoint_is_tls = bucket_config
            .and_then(|config| config.tls)
            .unwrap_or(true);
        
        dbg!("is_tls: {}", endpoint_is_tls);
        dbg!("endpoint: {}", &endpoint);

        let mut peer = Box::new(HttpPeer::new(addr, endpoint_is_tls, endpoint.clone()));
        dbg!("peer: {:#?}", &peer);

        // todo: make ths configurable

        peer.options.max_h2_streams = 128;
        peer.options.h2_ping_interval = Some(Duration::from_secs(30));


        // peer.options.idle_timeout          = Some(Duration::from_secs(300));
        // peer.options.connection_timeout    = Some(Duration::from_secs(30));
        // peer.options.read_timeout          = Some(Duration::from_secs(300));
        // peer.options.write_timeout         = Some(Duration::from_secs(300));

        debug!("peer: {:#?}", &peer);

        if let Some(verify) = self.verify {
            info!("Verify peer (upstream) certificates disabled!");
            peer.options.verify_cert = verify;
            peer.options.verify_hostname = verify;
        } else {
            peer.options.verify_cert = true;
        }

        debug!("peer: {:#?}", &peer);

        debug!("upstream_peer::end");
        Ok(peer)
    }


    async fn request_filter(&self, session: &mut Session, ctx: &mut Self::CTX) -> Result<bool> {
        debug!("request_filter::start");

        dbg!(&session.request_summary());

        dbg!(&session.req_header().uri);

        let request_query = session.req_header().uri.query().unwrap_or("");
        info!("request path: {}", session.req_header().uri.path());
        info!("request query: {}", request_query);
        info!("request method : {}", session.req_header().method);

        let parsed_query_result = parse_query(request_query);

        if parsed_query_result.is_err() {
            error!("Failed to parse query: {:?}", parsed_query_result);
            return Err(pingora::Error::new_str("Failed to parse query"));
        }
        let (rest, mut query_dict) = parsed_query_result.unwrap();
        if rest.is_empty() {
            info!("Parsed query: {:#?}", query_dict);
        } else {
            error!("Failed to parse query: {}", rest);
        }

        query_dict.insert("method".to_string(), session.req_header().method.to_string());
        query_dict.insert("path".to_string(), session.req_header().uri.path().to_string());
        // insert source
        query_dict.insert(
            "source".to_string(),
            session
                .req_header()
                .headers
                .get("x-forwarded-for")
                .and_then(|h| h.to_str().ok())
                .unwrap_or_default()
                .to_string(),
        );




        info!("---> Parsed query: {:#?}", query_dict);

        if session
            .req_header()
            .headers
            .get("expect")
            .map(|v| v.to_str().unwrap_or("").eq_ignore_ascii_case("100-continue"))
            .unwrap_or(false)
        {
            return Ok(false);
        };


        let path = session.req_header().uri.path();

        let parse_path_result = parse_path(path);
        if parse_path_result.is_err() {
            error!("Failed to parse path: {:?}", parse_path_result);
            return Err(pingora::Error::new_str("Failed to parse path"));
        }

        let (_, (bucket, _uri_path)) = parse_path_result.unwrap();

        let hdr_bucket = bucket.to_owned();

        let auth_header = session
            .req_header()
            .headers
            .get("authorization")
            .and_then(|h| h.to_str().ok())
            .map(ToString::to_string)
            .unwrap_or_default();

        let ttl = {
            let map = ctx.cos_mapping.read().await;
            map.get(bucket).and_then(|c| c.ttl).unwrap_or(0)
        };
        let mut access_key: String = String::new();

        if auth_header.is_empty() {
            if let Some(q) = session.req_header().uri.query() {
                if q.contains("X-Amz-Credential") {
                    let (_, p) = parse_presigned_params(&format!("?{q}"))
                        .map_err(|_| pingora::Error::new_str("Failed to parse presigned params"))?;
                    access_key = p.access_key.clone();
                }
            }
        } else {
            access_key = parse_token_from_header(&auth_header)
            .map_err(|_| pingora::Error::new_str("Failed to parse access_key"))?
            .1
            .to_string();
        }

        let is_authorized = if let Some(py_cb) = &ctx.validator {

            let is_multipart = session
                .req_header()
                .uri
                .query()
                .map_or(false, |q| q.contains("uploadId="));


            info!("CHECKING SIGNATURE");
            if let Some(skip) = self.skip_signature_validation {
                if skip || is_multipart {
                    info!("Skipping local signature check");
                    // continue
                    
                } else {
                    // presigned
                    info!("Checking presigned signature");
                    let uri_q = session.req_header().uri.query().unwrap_or("");

                    if auth_header.is_empty() && uri_q.contains("X-Amz-Signature") {
                        ctx.is_presigned = Some(true);

                        // ensure we have the secret_key in the keystore
                        if !ctx.hmac_keystore.read().await.contains_key(&access_key) {
                            debug!("No key in keystore, trying to fetch via hmac_fetcher for ->{}<-", access_key);
                            // fetch via hmac_fetcher exactly as you do below…
                            if let Some(py_fetcher) = &ctx.hmac_fetcher {
                                // call Python callback
                                let cb = py_fetcher;
                                let secret: PyResult<String> = Python::with_gil(|py| {
                                    cb.call1(py, (&access_key,))
                                      .and_then(|r| r.extract(py))
                                });
                                debug!("Got secret: {:#?}", secret);
                                match secret {
                                    Ok(secret_key) => {
                                        debug!("got key and inserting into keystore");
                                        ctx.hmac_keystore.write().await.insert(access_key.clone().to_string(), secret_key);
                                    }
                                    Err(_) => {
                                        // no key → unauthorized
                                        session.respond_error(401).await?;
                                        return Ok(true);
                                    }
                                }
                            } else {
                                session.respond_error(401).await?;
                                return Ok(true);
                            }
     
                        }
                        debug!("now checking if the signature is valid for presigned...");
                        let sk = ctx.hmac_keystore.read().await.get(&access_key).unwrap().clone();
                        debug!("got secret {} from keystore", sk);
                        debug!("RAW_PATH       = {}", &session.req_header().uri);
                        debug!("RAW_HOST_HDR   = {:?}", &session.req_header().headers.get("host"));
                        let ok = match signature_is_valid_for_presigned(&session, &sk).await {
                            Ok(b)  => b,
                            Err(e) => {
                                error!("presigned-URL validation error: {e}");   // <-- keep the info
                                return Err(pingora::Error::new_str("Failed to check signature"));
                            }
                        };                       
                        info!("is signature valid?: {}", ok);
                        if !ok {
                            session.respond_error(401).await?;
                            return Ok(true);
                        }
                    } else {
                    info!("processing a regular request");

                    let has_key = {
                        let map = ctx.hmac_keystore.read().await;
                        map.contains_key(&access_key)
                    };
                    if !has_key {
                        if let Some(py_fetcher) = &ctx.hmac_fetcher {
                            // call Python callback
                            let cb = py_fetcher;
                            let secret: PyResult<String> = Python::with_gil(|py| {
                                cb.call1(py, (&access_key,))
                                  .and_then(|r| r.extract(py))
                            });
                            match secret {
                                Ok(secret_key) => {
                                    ctx.hmac_keystore.write().await.insert(access_key.clone().to_string(), secret_key);
                                }
                                Err(_) => {
                                    // no key → unauthorized
                                    session.respond_error(401).await?;
                                    return Ok(true);
                                }
                            }
                        } else {
                            session.respond_error(401).await?;
                            return Ok(true);
                        }
                    }
                    let secret_key = {
                                let map = ctx.hmac_keystore.read().await;
                                map.get(&access_key).cloned()
                            };

                    info!("Checking signature");
                     let sig_ok = match signature_is_valid_for_request(
                         &auth_header,
                         &session,
                         &secret_key.unwrap(),
                     )
                     .await
                     {
                         Ok(true)  => true, 
                         Ok(false) => {
                             info!("Signature invalid");
                             false 
                         }
                         Err(err)  => {
                             error!("Signature check error: {}", err);
                             false
                         }
                     };
                     
                     // if signature failed, skip further validation
                     if !sig_ok {
                         session.respond_error(401).await?;
                         return Ok(true);
                     }
                    }
                }
            }
            info!("Signature check passed, continuing now onto the bespoke validation");
            let cache_key = format!("{}:{}:{:?}", &access_key, bucket, &query_dict);
            debug!("Cache key: {}", cache_key);

            let bucket_clone = bucket.to_string();
            let callback_clone: PyObject = Python::with_gil(|py| py_cb.clone_ref(py));

            let move_access_key = access_key.clone();
            let req = query_dict.clone();

            ctx.auth_cache
                .get_or_validate(&cache_key, Duration::from_secs(ttl), move || {
                    let tk = move_access_key.clone();
                    let bu = bucket_clone.clone();
                    let cb = Python::with_gil(|py| callback_clone.clone_ref(py));
                    {
                        let req_value = req.clone();
                        async move {
                            validate_request(&tk, &bu, &req_value, cb)
                                .await
                                .map_err(|_| pingora::Error::new_str("Validator error"))
                        }
                    }
                })
                .await?
        } else {
            true
        };

        if !is_authorized {
            info!("Access denied for bucket: {}.  End of request.", bucket);
            session.respond_error(401).await?;
            return Ok(true);
        }

        let bucket_config = {
            let map = ctx.cos_mapping.read().await;
            map.get(&hdr_bucket).cloned()
        };

        debug!("Access key: {}", &access_key);

        // we have to check for some available credentials here to be able to return unauthorized already if not
        match bucket_config.clone() {
            Some(mut config) => {
                let fetcher_opt = ctx.bucket_creds_fetcher.as_ref().map(|py_cb| {
                    // clone the PyObject so the async block is 'static
                    let cb = Python::with_gil(|py| py_cb.clone_ref(py));
                    move |bucket: String| async move {
                        get_credential_for_bucket(&cb, bucket, access_key)
                            .await
                            .map_err(|e| e.into()) // Convert PyErr → Box<dyn Error>
                    }
                });

                config
                    .ensure_credentials(&hdr_bucket, fetcher_opt)
                    .await
                    .map_err(|e| {
                        error!("Credential check failed for {hdr_bucket}: {e}");
                        pingora::Error::new_str("Credential check failed")
                    })?;

                ctx.cos_mapping
                    .write()
                    .await
                    .insert(hdr_bucket.clone(), config);
            }
            None => {
                error!("No configuration available for bucket: {hdr_bucket}");
                return Err(pingora::Error::new_str(
                    "No configuration available for bucket",
                ));
            }
        }
        debug!("request_filter::Credentials checked for bucket: {}. End of function.", hdr_bucket);
        debug!("request_filter::end");
        Ok(false)
    }

    async fn upstream_request_filter(
        &self,
        _session: &mut Session,
        upstream_request: &mut pingora::http::RequestHeader,
        ctx: &mut Self::CTX,
    ) -> Result<()> {

        if let Some(presigned) = ctx.is_presigned {
            if presigned {
                debug!("upstream_request_filter::presigned");
                let cleaned_q = upstream_request
                    .uri
                    .query()
                    .unwrap_or("")
                    .split('&')
                    .filter(|kv| !kv.starts_with("X-Amz-"))
                    .collect::<Vec<_>>()
                    .join("&");

            let _ = upstream_request.remove_header("authorization");
        
            let new_path_and_query = if cleaned_q.is_empty() {
                upstream_request.uri.path().to_owned()
            } else {
                format!("{}?{}", upstream_request.uri.path(), cleaned_q)
            };
        
            upstream_request.set_uri(new_path_and_query.try_into().unwrap());
 
            }
        };

        let _ = upstream_request.remove_header("accept-encoding");

        debug!("upstream_request_filter::start");


        let (_, (bucket, my_updated_url)) = parse_path(upstream_request.uri.path()).unwrap();

        dbg!(&my_updated_url);



        let hdr_bucket = bucket.to_string();

        let my_query = match upstream_request.uri.query() {
            Some(q) if !q.is_empty() => format!("?{}", q),
            _ => String::new(),
        };

        let bucket_config = {
            let map = ctx.cos_mapping.read().await;
            map.get(&hdr_bucket).cloned()
        };

        let addressing_style = bucket_config
            .clone()
            .and_then(|config| config.addressing_style)
            .unwrap_or("virtual".to_string());


        let this_url = match addressing_style.as_str() {
            "virtual" => my_updated_url,
            _ => {

                let u_url = format!("/{}{}", bucket, my_updated_url);
                dbg!("u_url: {}", &u_url);
                &u_url.clone()
            },
        };


        let endpoint = match bucket_config.clone() {
            Some(cfg) => {
                let this_host = match addressing_style.as_str() {
                    "path" => cfg.host.to_owned(),
                    _ => format!("{}.{}", bucket, cfg.host),
                };
                if cfg.port == 443 {
                    this_host
                } else {
                    format!("{}:{}", this_host, cfg.port)
                }
            }
            None => format!("{}.{}", bucket, self.cos_endpoint),
        };

        debug!("endpoint: {}.", &endpoint);

        // Box:leak the temporary string to get a static reference which will outlive the function
        let authority = Authority::from_static(Box::leak(endpoint.clone().into_boxed_str()));
        // if addressing_style == "virtual" {

        let new_uri = Uri::builder()
            .scheme("https")
            .authority(authority.clone())
            .path_and_query(this_url.to_owned() + &my_query)
            .build()
            .expect("should build a valid URI");

        upstream_request.set_uri(new_uri.clone());
        // }
        upstream_request.insert_header("host", authority.as_str())?;

        let (maybe_hmac, maybe_api_key) = match &bucket_config {
            Some(cfg) => (cfg.has_hmac(), cfg.api_key.clone()),
            None => (false, None),
        };

        let allowed = [
            "host",
            "content-length",
            "x-amz-date",
            "x-amz-content-sha256",
            "x-amz-security-token",
            // "content-md5",
            "transfer-encoding",
            "content-encoding",
            "x-amz-decoded-content-length",
            "x-amz-trailer",
            "x-amz-sdk-checksum-algorithm",
            "range",
            "expect",                      
            // "content-encoding",
            // "range",
            // "trailer",
            // "x-amz-trailer",
        ];


        let to_check: Vec<String> = upstream_request
            .headers
            .iter()
            .map(|(name, _)| name.as_str().to_owned())
            .collect();


        for name in to_check {
            let keep = allowed.contains(&name.as_str())
                || name.starts_with("x-amz-checksum-");
            if !keep {
                let _ = upstream_request.remove_header(&name);
            }
        }

        if maybe_hmac {
            debug!("HMAC: Signing request for bucket: {}", hdr_bucket);


            let streaming = {
                upstream_request
                    .headers
                    .get("x-amz-content-sha256")
                    .map(|v| v.as_bytes().starts_with(b"STREAMING-"))
                    .unwrap_or(false)
            };


            if streaming {

                let streaming_header = upstream_request
                    .headers
                    .get("x-amz-content-sha256")
                    .and_then(|v| v.to_str().ok())
                    .unwrap_or_default();

                dbg!("---".repeat(2000));
                debug!("streaming_header: {}", &streaming_header);

                dbg!("STREAMING UPLOAD");
                dbg!("*".repeat(2000));

                
                let access_key= bucket_config.as_ref().unwrap().access_key.as_ref().unwrap_or(&String::new()).to_string();
                let secret_key = bucket_config.as_ref().unwrap()
                    .secret_key
                    .as_ref()
                    .unwrap_or(&String::new())
                    .to_string();

                let region = bucket_config.as_ref().unwrap().region.as_ref().unwrap_or(&String::new()).to_string();

                // let decoded_len = upstream_request
                //     .headers
                //     .get("x-amz-decoded-content-length")
                //     .and_then(|v| v.to_str().ok())
                //     .unwrap_or("0")
                //     .to_owned();

                // remove the original streaming headers we cannot forward.
                // upstream_request.remove_header("x-amz-decoded-content-length");
                
                //  stream‑chunk.
                dbg!(&upstream_request.headers);
                upstream_request.remove_header("content-length");
                upstream_request.remove_header("content-md5");
                upstream_request.insert_header("transfer-encoding", "chunked")?;
                // upstream_request.insert_header("x-amz-decoded-content-length", decoded_len)?;
                upstream_request.set_send_end_stream(false);
                
                // produce *seed* signature and signing key that will be reused
                //    for every DATA frame in the forthcoming request_body_filter.
                let ts = chrono::Utc::now();
                resign_streaming_request(
                    upstream_request,
                    &region,
                    &access_key,
                    &secret_key,
                    ts,
                ).map_err(|e| {
                    error!("Failed to sign request: {e}");
                    pingora::Error::new_str("Failed to sign request")
                })?;
                
                let seed_sig = upstream_request
                    .headers
                    .get("authorization")
                    .and_then(|v| v.to_str().ok())
                    .and_then(|v| v.split("Signature=").nth(1))
                    .expect("seed signature missing")
                    .to_owned();
                
                // stash everything the body filter will need.
                ctx.stream_state = Some(
                    signer::StreamingState::new(
                        region.to_string(),
                        access_key.to_string(),
                        secret_key.to_string(),
                        ts,
                        seed_sig,
                    )
                );                
            } else {

                sign_request(upstream_request, bucket_config.as_ref().unwrap())
                    .await
                    .map_err(|e| {
                        error!("Failed to sign request for {}: {e}", hdr_bucket);
                        pingora::Error::new_str("Failed to sign request")
                    })?;
            }

            debug!("Request signed for bucket: {}", hdr_bucket);
            debug!("{:#?}", &upstream_request.headers);
        } else {
            debug!("Using API key for bucket: {}", hdr_bucket);
            let api_key = match maybe_api_key {
                Some(key) => key,
                None => {
                    // should be impossible because request_filter already
                    // called ensure_credentials, but double‑check anyway
                    error!("No API key for bucket {hdr_bucket}");
                    return Err(pingora::Error::new_str("No API key configured for bucket"));
                }
            };

            // closure captured by SecretsCache
            let bearer_fetcher = {
                let api_key = api_key.clone();
                move || get_bearer(api_key.clone())
            };

            let bearer_token = ctx
                .secrets_cache
                .get(&hdr_bucket, bearer_fetcher)
                .await
                .ok_or_else(|| pingora::Error::new_str("Failed to obtain bearer token"))?;

            upstream_request.insert_header("Authorization", format!("Bearer {bearer_token}"))?;
        }

        // debug!("Sending request to upstream: {}", &new_uri);

        debug!("Request sent to upstream.");
        debug!("upstream_request_filter::end");

        Ok(())
    }

    async fn response_filter(
        &self,
        _session: &mut Session,
        resp: &mut ResponseHeader,
        _ctx: &mut Self::CTX,
    ) -> Result<()> {
        let _ = resp.remove_header("server");

        let _ = resp.insert_header("Server", "Object-Storage-Proxy");

        Ok(())
    }

    async fn request_body_filter(
        &self,
        _session: &mut Session,
        body: &mut Option<bytes::Bytes>,
        end_of_stream: bool,
        ctx: &mut Self::CTX,
    ) -> Result<()> {
        // 0. Only active when we stashed a StreamingState in the request filter
        let Some(state) = ctx.stream_state.as_mut() else {
            return Ok(())
        };

        // 1. Flush frames are empty and *not* EOS - just ignore them
        let Some(payload) = body.take() else {
            return Ok(())
        };
        if payload.is_empty() && !end_of_stream {
            return Ok(())
        };

        // 2. Build the outgoing buffer
        let mut out = BytesMut::new();
        if !payload.is_empty() {
            out.extend_from_slice(&state.sign_chunk(&payload)
                                    .map_err(|e| {
                                        error!("Failed to sign chunk: {e}");
                                        pingora::Error::new_str("Failed to sign chunk")
                                    }
                                    )?)
                                        ;
        }
        if end_of_stream {
            out.extend_from_slice(&state.final_chunk()
                                    .map_err(|e| {
                                        error!("Failed to sign trailer: {e}");
                                        pingora::Error::new_str("Failed to sign trailer")
                                    }
                                )?);
            ctx.stream_state = None;          // upload finished
        }

        // 3. Hand the encoded bytes to Pingora
        *body = Some(out.freeze());
        Ok(())

    }

}

pub fn init_tracing() {
    tracing_subscriber::fmt()
        .with_timer(ChronoLocal::rfc_3339())
        .with_env_filter(EnvFilter::from_default_env())
        .init();
}

pub fn run_server(py: Python, run_args: &ProxyServerConfig) {
    init_tracing();

    if run_args.http_port.is_none() && run_args.https_port.is_none() {
        error!("At least one of http_port or https_port must be specified!");
        return;
    }

    if let Some(http_port) = run_args.http_port {
        info!("starting HTTP server on port {}", http_port);
    }

    if let Some(https_port) = run_args.https_port {
        info!("starting HTTPS server on port {}", https_port);
    }

    let local_hmac_map = if Python::with_gil(|py| run_args.hmac_keystore.is_none(py)) {
        HashMap::new()
    } else {
        parse_hmac_list(py, &run_args.hmac_keystore).unwrap_or(HashMap::new())
    };

    debug!("HMAC keys: {:#?}", &local_hmac_map);

    let cosmap = Arc::new(RwLock::new(parse_cos_map(py, &run_args.cos_map).unwrap()));
    let hmac_keystore = Arc::new(RwLock::new(local_hmac_map));

    let mut my_server = Server::new(None).unwrap();
    my_server.bootstrap();

    let validator = run_args.validator.as_ref().map(|v| v.clone_ref(py));
    let hmac_fetcher = run_args.hmac_fetcher.as_ref().map(|v| v.clone_ref(py));

    let mut my_proxy = pingora::proxy::http_proxy_service(
        &my_server.configuration,
        MyProxy {
            cos_endpoint: "s3.eu-de.cloud-object-storage.appdomain.cloud".to_string(),
            cos_mapping: Arc::clone(&cosmap),
            hmac_keystore: Arc::clone(&hmac_keystore),
            secrets_cache: SecretsCache::new(),
            auth_cache: AuthCache::new(),
            validator,
            bucket_creds_fetcher: run_args
                .bucket_creds_fetcher
                .as_ref()
                .map(|v| v.clone_ref(py)),
            verify: run_args.verify,
            skip_signature_validation: run_args.skip_signature_validation,
            hmac_fetcher
        },
    );

    if run_args.threads.is_some() {
        my_proxy.threads = run_args.threads;
    }

    debug!("Proxy service threads: {:?}", &my_proxy.threads);

    if let Some(http_port) = run_args.http_port {
        info!("starting HTTP server on port {}", &http_port);
        let addr = format!("0.0.0.0:{}", http_port);
        my_proxy.add_tcp(addr.as_str());
    }

    if let Some(https_port) = run_args.https_port {
        let cert_path =
            std::env::var("TLS_CERT_PATH").expect("Set TLS_CERT_PATH to the PEM certificate file");
        let key_path =
            std::env::var("TLS_KEY_PATH").expect("Set TLS_KEY_PATH to the PEM private-key file");

        let mut tls = pingora::listeners::tls::TlsSettings::intermediate(&cert_path, &key_path)
            .expect("failed to build TLS settings");

        tls.enable_h2();
        let https_addr = format!("0.0.0.0:{}", https_port);
        my_proxy.add_tls_with_settings(https_addr.as_str(), /*tcp_opts*/ None, tls);
    }
    
    my_server.add_service(my_proxy);

    debug!("{:?}", &my_server.configuration);

    py.allow_threads(|| my_server.run_forever());

    info!("server running ...");
}

/// Start an HTTP + HTTPS reverse‑proxy for IBM COS.
///
/// Equivalent to running ``pingora`` with a custom handler.
///
/// Parameters
/// ----------
/// run_args:
///    A :py:class:`ProxyServerConfig` object containing the configuration for the server.
///     The configuration includes the following parameters:
///   - cos_map: A dictionary mapping bucket names to their respective COS configuration.
///     Each entry should contain the following
///     keys:
///        - host: The COS endpoint (e.g., "s3.eu-de.cloud-object-storage.appdomain.cloud")
///        - port: The port number (e.g., 443)
///        - api_key/apikey: The API key for the bucket (optional)
///        - ttl/time-to-live: The time-to-live for the API key in seconds (optional)
///   - bucket_creds_fetcher: Optional Python async callable that fetches the API key for a bucket.
///     The callable should accept a single argument, the bucket name.
///     It should return a string containing the API key.
///   - http_port: The HTTP port to listen on.
///   - https_port: The HTTPS port to listen on.
///   - validator: Optional Python async callable that validates the request.
///     The callable should accept two arguments, the access_key and the bucket name.
///     It should return a boolean indicating whether the request is valid.
///   - threads: Optional number of threads to use for the server.
///     If not specified, the server will use a single thread.
#[pyfunction]
pub fn start_server(py: Python, run_args: &ProxyServerConfig) -> PyResult<()> {
    rustls::crypto::ring::default_provider()
        .install_default()
        .expect("Failed to install rustls crypto provider");

    dotenv().ok();

    run_server(py, run_args);

    Ok(())
}

#[pyfunction]
fn enable_request_counting() {
    REQ_COUNTER_ENABLED.store(true, Ordering::Relaxed);
}

#[pyfunction]
fn disable_request_counting() {
    REQ_COUNTER_ENABLED.store(false, Ordering::Relaxed);
}

#[pyfunction]
fn get_request_count() -> PyResult<usize> {
    Ok(REQ_COUNTER.load(Ordering::Relaxed))
}

#[pymodule]
fn object_storage_proxy(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(start_server, m)?)?;
    m.add_class::<ProxyServerConfig>()?;
    m.add_class::<CosMapItem>()?;
    m.add_function(wrap_pyfunction!(enable_request_counting, m)?)?;
    m.add_function(wrap_pyfunction!(disable_request_counting, m)?)?;
    m.add_function(wrap_pyfunction!(get_request_count, m)?)?;
    Ok(())
}
