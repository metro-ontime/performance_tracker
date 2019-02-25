#!/bin/bash

# Provide path of repo root directory as cmd line arg

docker pull ctsexton/performance_tracker
crontab $1/performance_tracker/setup/production_crontab
echo "New crontab config:"
crontab -l
