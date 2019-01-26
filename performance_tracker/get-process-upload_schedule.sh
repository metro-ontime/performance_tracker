#!/bin/bash
# Always execute this file with this directory as CWD

if [ $# -eq 0 ]
  then
    echo "Please provide your username as argument"
    exit 1
fi

bash ./get-process_schedule.sh $1

docker run -u $(id -u $1):$(id -g $1) --rm -v $(pwd):/src metro python upload_schedule.py
if [ $? -eq 0 ]; then
  echo "Successfully uploaded schedule to S3:" $(date)
else
  echo "Failed S3 upload:" $(date)
  exit 1
fi
