import os
import json
import requests
import pendulum
import pandas as pd

agency = "lametro-rail"
lines = range(801, 807)

for line in lines:
    now = pendulum.now("UTC")
    date = now.format("YYYY-MM-DD")
    time = now.format("HH:mm:ss")

    stops_direction_A = pd.read_csv(
        f"data/line_info/{line}/{line}_directionA_stations.csv", index_col=0
    )
    stops_direction_B = pd.read_csv(
        f"data/line_info/{line}/{line}_directionB_stations.csv", index_col=0
    )

    unique_stops = list(stops_direction_A.append(stops_direction_B).stop_id.unique())

    for stop_id in unique_stops:
        # url = f"http://api.metro.net/agencies/{agency}/routes/{line}/stops/{stop_id}/predictions/"
        url = f"http://webservices.nextbus.com/service/publicJSONFeed?command=predictions&a={agency}&routeTag={line}&stopId={stop_id}"
        response = requests.get(url)
        raw_data = response.json()

        directory_path = f"data/predictions/raw/{line}_{agency}/{stop_id}/{date}"
        os.makedirs(directory_path, exist_ok=True)

        with open(
            f"data/predictions/raw/{line}_{agency}/{stop_id}/{date}/{time}.json", "w"
        ) as outfile:
            json.dump(raw_data, outfile)
