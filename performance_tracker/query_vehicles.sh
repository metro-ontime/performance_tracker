#!/bin/bash
# Always execute this file with this directory as CWD

if [ $# -eq 0 ]
  then
    echo "Please provide your username as argument"
    exit 1
fi

docker run -u $(id -u $1):$(id -g $1) --rm -v $(pwd):/src metro python query_vehicles.py
if [ $? -eq 0 ]; then
  echo "Successfully downloaded vehicle data:" $(date) >> $(pwd)/logs/querylog
else
  echo "Failed vehicle data download:" $(date) >> $(pwd)/logs/querylog
  exit 1
fi
