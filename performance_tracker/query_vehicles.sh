#!/bin/bash

# Please provide root directory of performance_tracker repo as cmd line arg

docker run -u $(id -u ${USER}):$(id -u ${USER}) -it --rm -v $1:/src --name testrun metro python performance_tracker/query_vehicles.py
