import sys
import os
import json
import requests
import pendulum

agency = "lametro-rail"
lines = range(801, 807)

for line in lines:
    now = pendulum.now("UTC")
    date = now.format("YYYY-MM-DD")
    time = now.format("HH:mm:ss")

    url = f"http://webservices.nextbus.com/service/publicJSONFeed?command=vehicleLocations&a={agency}&r={line}"

    nextBusResponse = requests.get(url)
    raw_data = nextBusResponse.json()

    os.makedirs(f"data/vehicle_tracking/raw/{line}_{agency}/{date}", exist_ok=True)
    with open(
        f"data/vehicle_tracking/raw/{line}_{agency}/{date}/{time}.json", "w"
    ) as outfile:
        json.dump(raw_data, outfile)
