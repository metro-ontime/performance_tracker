#!/bin/bash

# Provide path of repo root directory as cmd line arg

docker build -t metro $1
crontab $1/performance_tracker/setup/production_crontab
echo "New crontab config:"
crontab -l
