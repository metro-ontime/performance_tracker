import os
import json
import pandas as pd
from library.analyzer.process_vehicles import (
    get_track,
    process_raw_vehicles
)
from library.helpers.timing import get_appropriate_timetable

def process_vehicles(ctx, datetime):
    agency = ctx.config["METRO_AGENCY"]
    lines = ctx.config["METRO_LINES"]
    date = datetime.in_tz(ctx.config["TIMEZONE"]).format("YYYY-MM-DD")
    preprocessed_path = ctx.tmp.get_abs_path(f"tracking/{agency}/preprocessed.csv")
    allData = pd.read_csv(preprocessed_path, index_col=0)

    for line in lines:
        try:
            lineData = allData[allData['line']==line] 
            tracks = get_track(line, ctx.config["LOCAL_DATA"])
            processed = process_raw_vehicles(lineData, tracks)
            ctx.tmp.write(f"tracking/{agency}/{line}/processed/{date}.csv", processed.to_csv())
        except Exception as e:
            print(datetime, e)
            continue

    return 0
