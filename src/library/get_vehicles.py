import sys
import os
import json
import requests
import pendulum

def get_vehicles(ctx):
    agency = ctx.config["METRO_AGENCY"]
    lines = ctx.config["METRO_LINES"]
    base_url = ctx.config["VEHICLE_API_URL"]
    for line in lines:
        data = get_vehicles_for_line(base_url, agency, line)
        ctx.tmp.write_json(f"tracking/{agency}/{line}/latest.json", data)
    return 0


def get_vehicles_for_line(base_url, agency, line):
    url = f"{base_url}?command=vehicleLocations&a={agency}&r={line}"
    return requests.get(url).json()
