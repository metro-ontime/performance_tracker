import os
import io
import requests
from zipfile import ZipFile

def get_schedule(ctx):
    url = ctx.config["schedule_url"]
    response = requests.get(url)
    zf = ZipFile(io.BytesIO(response.content))
    path = os.path.join(ctx.config["tmp_dir"], "GTFS")
    os.makedirs(path, exist_ok=True)
    zf.extractall(path)
    return "Successfully downloaded & extracted GTFS schedule data"
