#!/usr/bin/env python3.6
import glob
import os
import pandas as pd
import pendulum
import json
import sys
sys.path.append(os.path.dirname(sys.path[0]))
from library.analysis.nextbus import parse_nextbus_response
from library.helpers.timing import pandas_datetime_to_pendulum_datetime
from library.context import Context
from library.analyzer.schedule import scheduleTimeToDateTime

ctx = Context()
agency = ctx.config["METRO_AGENCY"]
path_to_data = os.environ["HISTORICAL_PATH"]

line = 801

# Get the month plus a day either side
start = pendulum.datetime(2018, 12, 31)
end = pendulum.datetime(2019, 2, 1)
period = pendulum.period(start, end)

df = pd.DataFrame(columns=["line", "vehicle_id","direction","report_time","latitude","longitude","predictable"])

for dt in period.range('days'):
    date = dt.format("YYYY-MM-DD")
    jsons = glob.glob(f"{path_to_data}/vehicle_tracking/raw/{line}_{agency}/{date}/*.json")
    for tracking_json in jsons:
        with open(os.path.abspath(tracking_json)) as nextbus_data:
            loaded_data = json.load(nextbus_data)
        try:
            parsed = parse_nextbus_response(loaded_data)
        except Exception as exc:
            ctx.logger(f"Error parsing and appending json data at {tracking_json}: {exc}")
            continue
        df = pd.concat([df, parsed], ignore_index=True, sort=False, join="inner")

df = df.dropna()
df.to_csv(f"{path_to_data}/test_month.csv")
