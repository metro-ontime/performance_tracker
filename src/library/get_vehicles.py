import sys
import os
import json
import requests
import pendulum

def get_vehicles(ctx):
    agency = ctx.config["metro_agency"]
    lines = ctx.config["metro_lines"]
    base_url = ctx.config["vehicle_api_url"]
    for line in lines:
        data = get_vehicles_for_line(base_url, agency, line)
        ctx.tmp.write(f"tracking/{agency}/{line}/latest.json", data)
    return "Successfully downloaded realtime vehicle data"


def get_vehicles_for_line(base_url, agency, line):
    url = f"{base_url}?command=vehicleLocations&a={agency}&r={line}"
    return requests.get(url).json()
