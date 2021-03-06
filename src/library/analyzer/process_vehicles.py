import json
import os
import sys

import pendulum
import pandas as pd
from shapely.geometry import LineString

from .geoHelpers import findRelativePositions, toGDF
from .tracker import getTrips


def load_track_by_direction(direction, line, path_base):
    track_path = os.path.join(path_base, f"line_info/{line}/{line}_{direction}.geojson")
    with open(track_path) as infile:
        obj = json.load(infile)
    return prepare_track(obj)

def prepare_track(track):
    return LineString(track["features"][0]["geometry"]["coordinates"])

def get_track(line, path_base):
    return [
        load_track_by_direction(direction, line, path_base) for direction in range(2)
    ]


def process_raw_vehicles(df, track):
    df = df.drop_duplicates(
        subset=["report_time", "latitude", "longitude", "vehicle_id"]
    )
    df = df[df["predictable"] == True]

    df["latitude"] = pd.to_numeric(df.latitude)
    df["longitude"] = pd.to_numeric(df.longitude)
    df = toGDF(df)

    mask_0 = (df["direction"] == 0) | (df["direction"] == 90)
    mask_1 = (df["direction"] == 180) | (df["direction"] == 270)
    df_0 = df.loc[mask_0]
    df_0 = df_0.assign(direction_id = 0)
    df_1 = df.loc[mask_1]
    df_1 = df_1.assign(direction_id = 1)
    df_0["relative_position"] = findRelativePositions(df_0, track[0])
    df_1["relative_position"] = findRelativePositions(df_1, track[1])
    df = pd.concat([df_0, df_1])

    df["datetime"] = pd.to_datetime(df["report_time"], utc=True)
    df["datetime_local_iso8601"] = df.report_time.apply(
        lambda dt: pendulum.parse(dt, tz="UTC")
        .in_tz("America/Los_Angeles")
        .to_iso8601_string()
    )
    df = df.reset_index(drop=True)  # necessary both before and after getTrips
    df = getTrips(df)
    df = df.reset_index(drop=True)  # necessary both before and after getTrips
    df["datetime"] = df["datetime_local_iso8601"]
    df = df[["datetime", "trip_id", "direction_id", "relative_position"]]
    return df
