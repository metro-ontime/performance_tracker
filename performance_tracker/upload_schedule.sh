#!/bin/bash
# Always execute this file with this directory as CWD

if [ $# -eq 0 ]
  then
    echo "Please provide your username as argument"
    exit 1
fi

docker run -u $(id -u $1):$(id -g $1) --rm -v $(pwd):/src metro python query_schedule.py
if [ $? -eq 0 ]; then
  echo "Successfully downloaded schedule data:" $(date) >> $(pwd)/logs/schedulelog
else
  echo "Failed schedule data download:" $(date) >> $(pwd)/logs/schedulelog
  exit 1
fi

docker run -u $(id -u $1):$(id -g $1) --rm -v $(pwd):/src metro python process_schedule.py
if [ $? -eq 0 ]; then
  echo "Successfully processed schedule data:" $(date) >> $(pwd)/logs/schedulelog
else
  echo "Failed schedule data processing:" $(date) >> $(pwd)/logs/schedulelog
  exit 1
fi

docker run \
  -u $(id -u $1):$(id -g $1) \
  --rm \
  -e AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID \
  -e AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY \
  -v $(pwd):/src metro python upload_schedule.py
if [ $? -eq 0 ]; then
  echo "Successfully uploaded schedule to S3:" $(date) >> $(pwd)/logs/uploadLog
else
  echo "Failed S3 upload:" $(date) >> $(pwd)/logs/uploadLog
  exit 1
fi
