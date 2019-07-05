import sys
import os
import json
import requests
import pendulum

def query_vehicles(ctx):
    agency = ctx.config["metro_agency"]
    lines = ctx.config["metro_lines"]
    for line in lines:
        now = pendulum.now("UTC")
        date = now.format("YYYY-MM-DD")
        time = now.format("HH:mm:ss")
        data = query_vehicles_for_line(agency, line)
        ctx.datastore.write(f"vehicle_tracking/raw/{line}_{agency}/{date}/{time}.json", data)


def query_vehicles_for_line(agency, line):
    url = f"http://webservices.nextbus.com/service/publicJSONFeed?command=vehicleLocations&a={agency}&r={line}"
    return requests.get(url).json()
