import os
import json
import pendulum
import pandas as pd
from analyzer.process_vehicles import (
    preprocess,
    determine_vehicle_paths,
    get_track,
    process_raw_vehicles,
)
from helpers.timing import get_appropriate_timetable

agency = "lametro-rail"
datetime = pendulum.now("America/Los_Angeles")


for line in range(801, 807):
    schedule = get_appropriate_timetable(datetime, f"data/schedule/{line}_{agency}")
    raw_vehicle_files = determine_vehicle_paths(
        f"data/vehicle_tracking/raw/{line}_{agency}", schedule["start"], schedule["end"]
    )
    array = [preprocess(path) for path in raw_vehicle_files]
    cleaned = [row for row in array if row is not None]
    df = pd.concat(cleaned)
    track = get_track(line, f"data/line_info/{line}")
    processed = process_raw_vehicles(df, track)
    date_format = schedule["start"].format("YYYY-MM-DD")
    processed_path_base = f"data/vehicle_tracking/processed/{line}_{agency}"
    processed_path = os.path.join(processed_path_base, date_format) + ".csv"
    os.makedirs(processed_path_base, exist_ok=True)
    processed.to_csv(processed_path)
