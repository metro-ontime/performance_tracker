#!/bin/bash

if [ $# -eq 0 ]
  then
    echo "Please provide your username as argument"
    exit 1
fi
docker run -it -p 8888:8888 --rm -v $(pwd):/home/$1/vol metro-dev
