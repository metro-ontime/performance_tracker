import os
import io
import requests
from zipfile import ZipFile

def get_schedule(ctx):
    url = ctx.config["SCHEDULE_URL"]
    response = requests.get(url)
    zf = ZipFile(io.BytesIO(response.content))
    path = os.path.join(ctx.config["TMP_DIR"], "GTFS")
    os.makedirs(path, exist_ok=True)
    zf.extractall(path)
    return 0
