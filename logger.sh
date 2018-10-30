#!/bin/bash

python ./logger.py
sqlite3 -header -csv ./log.db "SELECT * FROM metroLog_gold;" > ./metrolog.csv
sqlite3 -header -csv ./log.db "SELECT * FROM nextbusLog_gold;" > ./nextbuslog.csv