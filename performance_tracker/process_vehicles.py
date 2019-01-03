import os
import json
import pendulum
import pandas as pd
import geopandas as gpd
from shapely.geometry import LineString, Point
from analyzer.nextBusData import NextBusData
from analyzer.geoHelpers import findRelativePositions, toGDF
from analyzer.tracker import getTrips
from helpers.datetimefs import DateTimeFS, construct_filename

start_datetime = pendulum.today("America/Los_Angeles").add(hours=3)
end_datetime = pendulum.now("America/Los_Angeles")

line = 804
agency = "lametro-rail"

path_base = f"data/vehicle_tracking/raw/{line}_{agency}"

dtfs = DateTimeFS(path_base)

datetimes = dtfs.get_datetimes_in_range(
    start_datetime.in_tz("UTC"), end_datetime.in_tz("UTC")
)

track_northbound_path = f"data/line_info/{line}/{line}_northbound.geojson"
track_southbound_path = f"data/line_info/{line}/{line}_southbound.geojson"
with open(track_northbound_path) as infile:
    obj = json.load(infile)
    track_northbound = LineString(obj["features"][0]["geometry"]["coordinates"])
track_northbound
with open(track_southbound_path) as infile:
    track_southbound = json.load(infile)


def process_frame(datetime):
    source_path = construct_filename(path_base, datetime, ".json")
    with open(source_path, "r") as infile:
        raw_data = json.load(infile)
    preprocessed = NextBusData(raw_data)
    # no need to run any more processing
    # than necessary inside loop.
    return preprocessed.vehicles


array = [process_frame(datetime) for datetime in datetimes]
df = pd.concat(array)
df["latitude"] = pd.to_numeric(df.latitude)
df["longitude"] = pd.to_numeric(df.longitude)
df = toGDF(df)
df["relative_position"] = findRelativePositions(df, track_northbound)
df["datetime"] = pd.to_datetime(df["report_time"], utc=True)
df = df[df["predictable"] == "true"]
df = df.reset_index()
df = getTrips(df)

processed_path = f"data/vehicle_tracking/processed/{line}_{agency}"
os.makedirs(processed_path, exist_ok=True)
df.to_csv(os.path.join(processed_path, start_datetime.format("YYYY-MM-DD")) + ".csv")
