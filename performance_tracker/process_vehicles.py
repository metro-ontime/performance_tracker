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

agency = "lametro-rail"
now = pendulum.now("America/Los_Angeles")
today = now.format("YYYY-MM-DD")
yesterday = pendulum.yesterday("America/Los_Angeles").format("YYYY-MM-DD")
end_datetime = now

for line in range(801, 807):
    schedule_on_this_date = pd.read_csv(f"data/schedule/{line}_{agency}/{today}.csv")
    first_scheduled_arrival = pendulum.parse(
        schedule_on_this_date.datetime.min(), tz="America/Los_Angeles"
    )
    if now < first_scheduled_arrival:
        schedule_yesterday = pd.read_csv(
            f"data/schedule/{line}_{agency}/{yesterday}.csv"
        )
        start_datetime = pendulum.parse(
            schedule_yesterday.datetime.min(), tz="America/Los_Angeles"
        )
    else:
        start_datetime = first_scheduled_arrival

    path_base = f"data/vehicle_tracking/raw/{line}_{agency}"

    dtfs = DateTimeFS(path_base)

    datetimes = dtfs.get_datetimes_in_range(
        start_datetime.in_tz("UTC"), end_datetime.in_tz("UTC")
    )

    track_directionA_path = f"data/line_info/{line}/{line}_directionA.geojson"
    track_directionB_path = f"data/line_info/{line}/{line}_directionB.geojson"
    with open(track_directionA_path) as infile:
        obj = json.load(infile)
        track_directionA = LineString(obj["features"][0]["geometry"]["coordinates"])
    track_directionA
    with open(track_directionB_path) as infile:
        track_directionB = json.load(infile)

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
    df["relative_position"] = findRelativePositions(df, track_directionA)
    df["datetime"] = pd.to_datetime(df["report_time"], utc=True)
    df = df[df["predictable"] == "true"]
    df = df.reset_index()
    df = getTrips(df)

    processed_path = f"data/vehicle_tracking/processed/{line}_{agency}"
    os.makedirs(processed_path, exist_ok=True)
    df.to_csv(
        os.path.join(processed_path, start_datetime.format("YYYY-MM-DD")) + ".csv"
    )
