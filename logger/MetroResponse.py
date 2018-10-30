import json
import pandas as pd
from datetime import datetime
import pytz

class MetroResponse:
    def __init__(self, data):
        self.vehicles = get_vehicles(data)
        self.timestamp = get_timestamp(data)

def get_vehicles(data):
    obj = json.loads(data.read())
    df = pd.DataFrame(obj['items'])
    df = matchColumnNames(df)
    return df[['vehicle_id', 'direction', 'seconds_since_report', 'latitude', 'longitude']]

def get_timestamp(data):
    time_string = data.info()['Date']
    date_obj = datetime.strptime(time_string, '%a, %d %b %Y %H:%M:%S %Z')
    timezone = pytz.timezone("GMT")
    date_obj = timezone.localize(date_obj)
    return date_obj.timestamp()

def matchColumnNames(df):
    return df.rename(columns={"id": "vehicle_id", "heading": "direction"})
    
