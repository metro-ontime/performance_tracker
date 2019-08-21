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
    data = requests.get(url).json()
    # The JSON returned from this API is not valid.
    # It returns booleans as strings.
    # We need to change every "true" to True and "false" to False
    data = fix_bools(data)
    return data

def fix_bools(thing):
    if isinstance(thing, dict):
        for k, v in thing.items():
            thing[k] = fix_bools(v)
    elif isinstance(thing, list):
        thing = [fix_bools(v) for v in thing]
    elif thing == 'true':
        thing = True
    elif thing == 'false':
        thing = False
    return thing
