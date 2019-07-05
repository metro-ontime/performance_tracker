#!/bin/bash
# Always execute this file with this directory as CWD

if [ $# -eq 0 ]
  then
    echo "Please provide your username as argument"
    exit 1
fi

# We limit cpu usage to 50% as this process is resource intensive 
# and we don't mind if it takes a few minutes extra to run
docker run --cpus=".75" -u $(id -u $1):$(id -g $1) --rm -v $(pwd):/src metro python -u process_vehicles.py
if [ $? -eq 0 ]; then
  echo "Successfully processed vehicles:" $(date)
else
  echo "Failed to process vehicles:" $(date)
  exit 1
fi

