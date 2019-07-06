import os
import io
import requests
from zipfile import ZipFile

def get_schedule(ctx):
    url = "https://gitlab.com/LACMTA/gtfs_rail/raw/master/gtfs_rail.zip"
    response = requests.get(url)
    zf = ZipFile(io.BytesIO(response.content))
    path = os.path.join(ctx.config["local_data"], "GTFS")
    os.makedirs(path, exist_ok=True)
    zf.extractall(path)
    return "Successfully downloaded & extracted GTFS schedule data"
