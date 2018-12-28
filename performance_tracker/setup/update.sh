#!/bin/bash

cd $1
python3 -m venv venv
source venv/bin/activate
pip install cython
pip install numpy
pip install pyproj
pip install -r requirements.txt
deactivate
