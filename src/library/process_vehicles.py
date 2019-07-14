import os
import json
import pendulum
import pandas as pd
from analyzer.process_vehicles import (
    prepare_track,
    process_raw_vehicles
)
from helpers.timing import get_appropriate_timetable

def process_vehicles(ctx, datetime):
    agency = ctx.config["metro_agency"]
    lines = ctx.config["metro_lines"]
    date = datetime.in_tz(ctx.config["timezone"]).format("YYYY-MM-DD")
    for line in lines:
        raw_df = ctx.datastore.read_csv(f"vehicle_tracking/raw/{line}_{agency}/{date}.csv")
        track = get_track(ctx, line)
        processed = process_raw_vehicles(raw_df, track)
        ctx.datastore.write(f"vehicle_tracking/processed/{line}_{agency}/", processed.to_csv())
    return 0

def get_track(ctx, line):
    return [
        prepare_track(ctx.datastore.read_local(
            f"line_info/{line}/{line}_{direction}.geojson"
        ))
        for direction in range(2)
    ]
