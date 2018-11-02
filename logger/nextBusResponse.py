import json
import pandas as pd
from datetime import datetime

class NextBusResponse:
    def __init__(self, data):
        obj = json.loads(data.read())
        self.timestamp = get_timestamp(obj)
        self.vehicles = get_vehicles(obj, self.timestamp)

def get_vehicles(data, timestamp):
    df = pd.DataFrame(data['vehicle'])
    df = matchColumnNames(df)
    df['query_time'] = df.vehicle_id.apply(lambda row: timestamp)
    return df[['vehicle_id', 'direction', 'query_time', 'seconds_since_report', 'latitude', 'longitude', 'predictable']]

def get_timestamp(data):
    return int(data['lastTime']['time']) / 1000

def matchColumnNames(df):
    return df.rename(columns={"id": "vehicle_id", "heading": "direction", "secsSinceReport": "seconds_since_report", "lat": "latitude", "lon": "longitude"})
    
