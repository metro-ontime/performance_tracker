#!/bin/bash

python ./log_vehicle_positions.py lametro-rail 804
sqlite3 -header -csv ./data/log.db "SELECT * FROM metroLog_gold;" > ./data/metrolog.csv
sqlite3 -header -csv ./data/log.db "SELECT * FROM nextbusLog_gold;" > ./data/nextbuslog.csv
