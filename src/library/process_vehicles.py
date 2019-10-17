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
    processed_path = ctx.tmp.get_abs_path(f"tracking/{agency}/processed.csv")

    allData = pd.read_csv(preprocessed_path, index_col=0)

    try:
        df = pd.read_csv(processed_path, index_col=0)
    except:
        df = pd.DataFrame(columns=["datetime", "trip_id", "direction_id", "relative_position"])

    for line in lines:
        try:
            #path = ctx.tmp.get_abs_path(f"tracking/{agency}/{line}/preprocessed.csv")
            lineData = allData[allData['line']==line] 
            tracks = get_track(line, ctx.config["LOCAL_DATA"])
            processed = process_raw_vehicles(lineData, tracks)
            df = pd.concat([df, processed], ignore_index=True, sort=False, join="inner")
        except Exception as e:
            print(datetime, e)
            continue
        ctx.tmp.write(f"tracking/{agency}/{line}/processed.csv", processed.to_csv())
    return 0
