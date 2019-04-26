import json
import os
import sys

sys.path.append("..")

import pendulum
import pandas as pd
import geopandas as gpd
from shapely.geometry import LineString

from analyzer.geoHelpers import findRelativePositions, toGDF
from analyzer.tracker import getTrips
from analyzer.nextBusData import NextBusData
from helpers.datetimefs import DateTimeFS


def determine_vehicle_paths(vehicle_path_base, start_datetime, end_datetime):
    dtfs = DateTimeFS(vehicle_path_base)
    return dtfs.get_filenames_in_range(
        ".json", start_datetime.in_tz("UTC"), end_datetime.in_tz("UTC")
    )


def preprocess(path):
    with open(path, "r") as infile:
        raw_data = json.load(infile)
    try:
        preprocessed = NextBusData(raw_data)
    except:
        return None
    return preprocessed.vehicles


def load_track_by_direction(direction, line, path_base):
    track_path = f"{path_base}/{line}_{direction}.geojson"
    with open(track_path) as infile:
        obj = json.load(infile)
    return LineString(obj["features"][0]["geometry"]["coordinates"])


def get_track(line, path_base):
    return [
        load_track_by_direction(direction, line, path_base) for direction in range(2)
    ]


def process_raw_vehicles(df, track):
    df = df.drop_duplicates(
        subset=["report_time", "latitude", "longitude", "vehicle_id"]
    )
    df = df[df["predictable"] == "true"]

    df["latitude"] = pd.to_numeric(df.latitude)
    df["longitude"] = pd.to_numeric(df.longitude)
    df = toGDF(df)

    mask_0 = (df["direction"] == "0") | (df["direction"] == "90")
    mask_1 = (df["direction"] == "180") | (df["direction"] == "270")
    df_0 = df.loc[mask_0]
    df_1 = df.loc[mask_1]

    # TODO: We can cache the results of findRelativePositions since there is a finite set of sensor locations.
    df_0["relative_position"] = findRelativePositions(df_0, track[0])
    df_0["direction_id"] = 0
    df_1["relative_position"] = findRelativePositions(df_1, track[1])
    df_1["direction_id"] = 1
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
