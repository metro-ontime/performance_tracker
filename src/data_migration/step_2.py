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
from library.helpers.timing import get_appropriate_timetable

ctx = Context()
line = 801
agency = ctx.config["METRO_AGENCY"]
path_to_data = os.environ["HISTORICAL_PATH"]
schedule_base_path = f"{path_to_data}/schedule/{line}_{agency}"

# Get the month plus a day either side
start = pendulum.datetime(2019, 1, 26, tz=ctx.config['TIMEZONE'])
end = pendulum.datetime(2019, 1, 31, tz=ctx.config['TIMEZONE'])
period = pendulum.period(start, end)

df = pd.read_csv(f"{path_to_data}/test_month.csv", parse_dates=['report_time'])

for date in period.range('days'):
    schedule = get_appropriate_timetable(date.add(hours=12), schedule_base_path, ctx)
    next_schedule = get_appropriate_timetable(date.add(hours=36), schedule_base_path, ctx)
    date_formatted = date.format("YYYY-MM-DD")
    schedule_start = schedule.datetime.min()
    next_schedule_start = next_schedule.datetime.min()
    
    mask = (df['report_time'] >= schedule_start) & (df['report_time'] < next_schedule_start)
    df_today = df.loc[mask]
    df_today.to_csv(f"{path_to_data}/preprocessed/{line}_{agency}/{date_formatted}.csv", index=False)

