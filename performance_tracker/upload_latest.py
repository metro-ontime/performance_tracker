from helpers.upload import upload
import pendulum
from helpers.timing import get_appropriate_timetable


now = pendulum.now("America/Los_Angeles")
agency = "lametro-rail"

for line in range(801, 807):
    schedule_base_path = f"data/schedule/{line}_{agency}"
    schedule_meta = get_appropriate_timetable(now, schedule_base_path)
    date = schedule_meta["date"]
    summary_path = f"data/summaries/{line}_{agency}/{date}.json"
    positions_path = f"data/vehicle_tracking/processed/{line}_{agency}/{date}.csv"
    upload(summary_path, summary_path)
    upload(positions_path, positions_path)
