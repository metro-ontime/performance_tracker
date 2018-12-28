#!/bin/bash

source ../env/bin/activate
python3 ./query_vehicles.py lametro-rail 801
python3 ./query_vehicles.py lametro-rail 802
python3 ./query_vehicles.py lametro-rail 803
python3 ./query_vehicles.py lametro-rail 804
python3 ./query_vehicles.py lametro-rail 805
python3 ./query_vehicles.py lametro-rail 806
deactivate
