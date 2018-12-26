import os
import json
import pendulum
import pandas as pd
from analyzer.nextBusData import NextBusData
from analyzer.datetimefs import DateTimeFS, construct_filename

start_datetime = pendulum.today("UTC")
end_datetime = pendulum.now("UTC")

line = 804
agency = "lametro-rail"

path_base = f"data/vehicle_tracking/raw/{line}_{agency}"

dtfs = DateTimeFS(path_base)

datetimes = dtfs.get_datetimes_in_range(start_datetime, end_datetime)


def process_frame(datetime):
    source_path = construct_filename(path_base, datetime, ".json")
    with open(source_path, "r") as infile:
        raw_data = json.load(infile)
    preprocessed = NextBusData(raw_data)
    return preprocessed.vehicles


array = [process_frame(datetime) for datetime in datetimes]
df = pd.concat(array)

processed_path = f"data/vehicle_tracking/processed/{line}_{agency}"
os.makedirs(processed_path, exist_ok=True)
df.to_csv(os.path.join(processed_path, start_datetime.format("YYYY-MM-DD")) + ".csv")
