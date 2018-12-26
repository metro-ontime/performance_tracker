#!/bin/bash

source env/bin/activate
python ./download_raw_data.py lametro-rail 801
python ./download_raw_data.py lametro-rail 802
python ./download_raw_data.py lametro-rail 803
python ./download_raw_data.py lametro-rail 804
python ./download_raw_data.py lametro-rail 805
python ./download_raw_data.py lametro-rail 806
deactivate
