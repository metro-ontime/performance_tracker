#!/bin/bash

if [ $# -eq 0 ]
  then
    echo "Please provide your username as argument"
    exit 1
fi
cp ../requirements.txt ./requirements.txt
docker build -t metro-dev --build-arg=NB_USER=$1 .

if [ $? -eq 0 ]; then
    echo "Build succeeded, start dev environment by executing start-dev.sh"
    rm ./requirements.txt
else
    echo "Build failed"
    rm ./requirements.txt
    exit 1
fi
