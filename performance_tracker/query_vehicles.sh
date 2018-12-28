#!/bin/bash

# Please provide username and root directory of performance_tracker repo as cmd line args

docker run -u $(id -u $1):$(id -g $1) --rm -v $2:/src metro python performance_tracker/query_vehicles.py
echo "query_vehicles.sh completed:" $(date) >> ~/logs/querylog
