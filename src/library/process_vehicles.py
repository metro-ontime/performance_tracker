import os
import json
import pandas as pd
from library.analyzer.process_vehicles import (
    get_track,
    process_raw_vehicles
)
from library.helpers.timing import get_appropriate_timetable

def process_vehicles(ctx, datetime):
    agency = ctx.config["metro_agency"]
    lines = ctx.config["metro_lines"]
    date = datetime.in_tz(ctx.config["timezone"]).format("YYYY-MM-DD")
    for line in lines:
        path = ctx.tmp.get_abs_path(f"tracking/{agency}/{line}/preprocessed.csv")
        df = pd.read_csv(path, index_col=0)
        tracks = get_track(line, ctx.config["local_data"])
        processed = process_raw_vehicles(df, tracks)
        ctx.tmp.write(f"tracking/{agency}/{line}/processed.csv", processed.to_csv())
    return 0
