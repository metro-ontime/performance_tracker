#!/bin/bash

source ../env/bin/activate
python ./query_vehicles.py lametro-rail 801
python ./query_vehicles.py lametro-rail 802
python ./query_vehicles.py lametro-rail 803
python ./query_vehicles.py lametro-rail 804
python ./query_vehicles.py lametro-rail 805
python ./query_vehicles.py lametro-rail 806
deactivate
