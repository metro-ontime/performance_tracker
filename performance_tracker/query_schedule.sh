#!/bin/bash
# Always execute this file with this directory as CWD

if [ $# -eq 0 ]
  then
    echo "Please provide your username as argument"
    exit 1
fi

docker run -u $(id -u $1):$(id -g $1) --rm -v $(pwd):/src metro python query_schedule.py
if [ $? -eq 0 ]; then
  echo "Successfully downloaded schedule data:" $(date)
else
  echo "Failed schedule data download:" $(date)
  exit 1
fi

docker run -u $(id -u $1):$(id -g $1) --rm -v $(pwd):/src metro python process_schedule.py
if [ $? -eq 0 ]; then
  echo "Successfully processed schedule data:" $(date)
else
  echo "Failed schedule data processing:" $(date)
  exit 1
fi
