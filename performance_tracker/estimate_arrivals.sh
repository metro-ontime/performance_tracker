#!/bin/bash
# Always execute this file with this directory as CWD

if [ $# -eq 0 ]
  then
    echo "Please provide your username as argument"
    exit 1
fi

# We limit cpu usage to 50% as this process is resource intensive 
# and we don't mind if it takes a few minutes extra to run
docker run --cpus=".5" -u $(id -u $1):$(id -g $1) --rm -v $(pwd):/src metro python -u estimate_arrivals.py
if [ $? -eq 0 ]; then
  echo "Successfully estimated arrivals:" $(date)
else
  echo "Failed to estimate arrivals:" $(date)
  exit 1
fi

