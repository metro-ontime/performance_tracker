import glob
import pendulum
import os
import pandas as pd
import geopandas as gpd
import json
from shapely.geometry import LineString, Point
from analyzer.geoHelpers import findRelativePositions

track_stations = {}
stops = pd.read_csv("data/GTFS/stops.txt")
agency = "lametro-rail"
# Run this file only after running process_schedule.py on the same day
datestring = pendulum.today("America/Los_Angeles").format("YYYY-MM-DD")

for line_no in range(801, 807):
    trackpaths = glob.glob(f"data/line_info/{line_no}/*.geojson")
    for path in trackpaths:
        name = os.path.basename(path).split(".")[0]
        with open(path) as data:
            track = LineString(
                json.load(data)["features"][0]["geometry"]["coordinates"]
            )
        schedule = pd.read_csv(f"data/schedule/{line_no}_{agency}/{datestring}.csv")
        stations = [str(station) for station in schedule["stop_id"].unique()]
        line_stops = stops[stops["stop_id"].isin(stations)][
            ["stop_id", "stop_name", "stop_lat", "stop_lon"]
        ]
        gdf = gpd.GeoDataFrame(
            line_stops,
            geometry=[
                Point(xy) for xy in zip(line_stops.stop_lon, line_stops.stop_lat)
            ],
        )
        gdf = gdf.drop(["stop_lat", "stop_lon"], axis=1)
        gdf.loc[:, "relative_position"] = findRelativePositions(gdf, track)
        track_stations[name] = gdf

# Blue line (801) has a different set of stations for each direction
# due to a small loop.
# We remove them here:
edit = track_stations["801_directionA"]
track_stations["801_directionA"] = edit[
    (edit["stop_id"].isin(["80153", "80154"]) == False)
]
edit = track_stations["801_directionB"]
track_stations["801_directionB"] = edit[(edit["stop_id"].isin(["80102"]) == False)]

for name in track_stations.keys():
    track_stations[name] = (
        track_stations[name]
        .sort_values("relative_position")
        .reset_index()
        .drop(["index"], axis=1)
    )

for name, station_list in track_stations.items():
    line_no = name.split("_")[0]
    os.makedirs(f"data/line_info/{line_no}", exist_ok=True)
    path = f"data/line_info/{line_no}/{name}_stations.csv"
    station_list.to_csv(path)
