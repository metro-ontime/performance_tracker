from helpers.upload import upload
import pendulum
from helpers.timing import get_appropriate_timetable


now = pendulum.now("America/Los_Angeles")
agency = "lametro-rail"

for line in range(801, 807):
    vehicles_base_path = f"data/vehicle_tracking/processed/{line}_{agency}"
    vehicles_meta = get_appropriate_timetable(now, vehicles_base_path)
    date = vehicles_meta["date"]
    positions_path = vehicles_meta["path"]
    upload(positions_path, positions_path)

summary_path = f"data/summaries/{date}.json"
upload(summary_path, summary_path)
