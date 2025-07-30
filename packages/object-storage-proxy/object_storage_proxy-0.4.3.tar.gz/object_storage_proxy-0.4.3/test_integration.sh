#!/usr/bin/env bash

# cd /Users/jeroen/projects/mandelbrot

echo -e "AWS_REQUEST_CHECKSUM_CALCULATION=WHEN_REQUIRED"
export AWS_REQUEST_CHECKSUM_CALCULATION=WHEN_REQUIRED


echo -e "\033[1;37m SSL (osps)\033[0m"
echo -e "\033[1;34m ----------\033[0m\n"

echo -e "\033[1;34mAWS\033[0m\n"
echo "generate testfile"
dd if=/dev/random of=/Users/jeroen/projects/mandelbrot/testfile_10 bs=1M count=10

echo "uploading 10MB file."
aws s3 cp testfile_10 s3://proxy-aws-bucket01/mandelbrot/testfile_10bis --profile osps
if [ $? -eq 0 ]; then
    echo -e "\033[1;32mOK\033[0m"
else
    echo -e "\033[1;31mERROR\033[0m"
fi
echo "listing .."
aws s3 ls s3://proxy-aws-bucket01/mandelbrot/testfile_10bis --profile osps
if [ $? -eq 0 ]; then
    echo -e "\033[1;32mOK\033[0m"
else
    echo -e "\033[1;31mERROR\033[0m"
fi

echo "download a 10MB file"
aws s3 cp s3://proxy-aws-bucket01/mandelbrot/testfile_10bis testfile_10bis --profile osps
if [ $? -eq 0 ]; then
    echo -e "\033[1;32mOK\033[0m"
else
    echo -e "\033[1;31mERROR\033[0m"
fi

echo "listing .."
ls -latrh testfile_10bis

if [ $? -eq 0 ]; then
    echo -e "\033[1;32mOK\033[0m"
else
    echo -e "\033[1;31mERROR\033[0m"
fi

echo "deleting .."
aws s3 rm s3://proxy-aws-bucket01/mandelbrot/testfile_10bis --profile osps
if [ $? -eq 0 ]; then
    echo -e "\033[1;32mOK\033[0m"
else
    echo -e "\033[1;31mERROR\033[0m"
fi

echo "listing .."
aws s3 ls s3://proxy-aws-bucket01/mandelbrot/testfile_10bis --profile osps
if [ $? -eq 1 ]; then
    echo -e "\033[1;32mOK\033[0m"
else
    echo -e "\033[1;31mERROR\033[0m"
fi

echo -e "\n\033[1;34mIBM\033[0m\n"

echo "uploading 10MB file."
aws s3 cp testfile_10 s3://proxy-bucket01/mandelbrot/testfile_10bis --profile osps
if [ $? -eq 0 ]; then
    echo -e "\033[1;32mOK\033[0m"
else
    echo -e "\033[1;31mERROR\033[0m"
fi
echo "listing .."
aws s3 ls s3://proxy-bucket01/mandelbrot/testfile_10bis --profile osps
if [ $? -eq 0 ]; then
    echo -e "\033[1;32mOK\033[0m"
else
    echo -e "\033[1;31mERROR\033[0m"
fi

echo "download a 10MB file"
aws s3 cp s3://proxy-bucket01/mandelbrot/testfile_10bis testfile_10bis --profile osps
if [ $? -eq 0 ]; then
    echo -e "\033[1;32mOK\033[0m"
else
    echo -e "\033[1;31mERROR\033[0m"
fi

echo "listing downloaded file .."
ls -latrh testfile_10bis

if [ $? -eq 0 ]; then
    echo -e "\033[1;32mOK\033[0m"
else
    echo -e "\033[1;31mERROR\033[0m"
fi

echo "deleting .."
aws s3 rm s3://proxy-bucket01/mandelbrot/testfile_10bis --profile osps
if [ $? -eq 0 ]; then
    echo -e "\033[1;32mOK\033[0m"
else
    echo -e "\033[1;31mERROR\033[0m"
fi

echo "listing .."
aws s3 ls s3://proxy-bucket01/mandelbrot/testfile_10bis --profile osps
if [ $? -eq 1 ]; then
    echo -e "\033[1;32mOK\033[0m"
else
    echo -e "\033[1;31mERROR\033[0m"
fi

echo -e "\n\033[1;37m no SSL (osp)\033[0m"
echo -e "\n\033[1;37m ------------\033[0m\n"


echo -e "\033[1;34mAWS\033[0m\n"
echo "generate testfile"
dd if=/dev/random of=/Users/jeroen/projects/mandelbrot/testfile_10 bs=1M count=10

echo "uploading 10MB file."
aws s3 cp testfile_10 s3://proxy-aws-bucket01/mandelbrot/testfile_10bis --profile osp
if [ $? -eq 0 ]; then
    echo -e "\033[1;32mOK\033[0m"
else
    echo -e "\033[1;31mERROR\033[0m"
fi
echo "listing .."
aws s3 ls s3://proxy-aws-bucket01/mandelbrot/testfile_10bis --profile osp
if [ $? -eq 0 ]; then
    echo -e "\033[1;32mOK\033[0m"
else
    echo -e "\033[1;31mERROR\033[0m"
fi

echo "download a 10MB file"
aws s3 cp s3://proxy-aws-bucket01/mandelbrot/testfile_10bis testfile_10bis --profile osp
if [ $? -eq 0 ]; then
    echo -e "\033[1;32mOK\033[0m"
else
    echo -e "\033[1;31mERROR\033[0m"
fi

echo "listing .."
ls -latrh testfile_10bis

if [ $? -eq 0 ]; then
    echo -e "\033[1;32mOK\033[0m"
else
    echo -e "\033[1;31mERROR\033[0m"
fi

echo "deleting .."
aws s3 rm s3://proxy-aws-bucket01/mandelbrot/testfile_10bis --profile osp
if [ $? -eq 0 ]; then
    echo -e "\033[1;32mOK\033[0m"
else
    echo -e "\033[1;31mERROR\033[0m"
fi

echo "listing .."
aws s3 ls s3://proxy-aws-bucket01/mandelbrot/testfile_10bis --profile osp
if [ $? -eq 1 ]; then
    echo -e "\033[1;32mOK\033[0m"
else
    echo -e "\033[1;31mERROR\033[0m"
fi

echo -e "\n\033[1;34mIBM\033[0m\n"

echo "uploading 10MB file."
aws s3 cp testfile_10 s3://proxy-bucket01/mandelbrot/testfile_10bis --profile osp
if [ $? -eq 0 ]; then
    echo -e "\033[1;32mOK\033[0m"
else
    echo -e "\033[1;31mERROR\033[0m"
fi

echo "listing .."
aws s3 ls s3://proxy-bucket01/mandelbrot/testfile_10bis --profile osp
if [ $? -eq 0 ]; then
    echo -e "\033[1;32mOK\033[0m"
else
    echo -e "\033[1;31mERROR\033[0m"
fi

echo "download a 10MB file"
aws s3 cp s3://proxy-bucket01/mandelbrot/testfile_10bis testfile_10bis --profile osp
if [ $? -eq 0 ]; then
    echo -e "\033[1;32mOK\033[0m"
else
    echo -e "\033[1;31mERROR\033[0m"
fi

echo "listing downloaded file .."
ls -latrh testfile_10bis

if [ $? -eq 0 ]; then
    echo -e "\033[1;32mOK\033[0m"
else
    echo -e "\033[1;31mERROR\033[0m"
fi

echo "deleting .."
aws s3 rm s3://proxy-bucket01/mandelbrot/testfile_10bis --profile osp
if [ $? -eq 0 ]; then
    echo -e "\033[1;32mOK\033[0m"
else
    echo -e "\033[1;31mERROR\033[0m"
fi

echo "listing .."
aws s3 ls s3://proxy-bucket01/mandelbrot/testfile_10bis --profile osp
if [ $? -eq 1 ]; then
    echo -e "\033[1;32mOK\033[0m"
else
    echo -e "\033[1;31mERROR\033[0m"
fi