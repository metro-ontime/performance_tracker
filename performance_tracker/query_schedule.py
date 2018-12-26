import os
import io
import requests
import zipfile

os.makedirs("data/GTFS", exist_ok=True)
url = "https://gitlab.com/LACMTA/gtfs_rail/raw/master/gtfs_rail.zip"

response = requests.get(url)
z = zipfile.ZipFile(io.BytesIO(response.content))
z.extractall("data/GTFS")
