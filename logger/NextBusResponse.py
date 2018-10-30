import json
import pandas as pd
from datetime import datetime

class NextBusResponse:
    def __init__(self, data):
        obj = json.loads(data.read())
        self.vehicles = get_vehicles(obj)
        self.timestamp = get_timestamp(obj)

def get_vehicles(data):
    df = pd.DataFrame(data['vehicle'])
    df = matchColumnNames(df)
    return df[['vehicle_id', 'direction', 'seconds_since_report', 'latitude', 'longitude']]

def get_timestamp(data):
    return int(data['lastTime']['time']) / 1000

def matchColumnNames(df):
    return df.rename(columns={"id": "vehicle_id", "heading": "direction", "secsSinceReport": "seconds_since_report", "lat": "latitude", "lon": "longitude"})
    
