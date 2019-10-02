import pendulum
from library.helpers.timing import get_appropriate_timetable

def upload_latest(ctx, dt):
    agency = "lametro-rail"

    for line in range(801, 807):
        vehicles_base_path = f"data/vehicle_tracking/processed/{line}_{agency}"
        vehicles_meta = get_appropriate_timetable(dt, vehicles_base_path)
        date = vehicles_meta["date"]
        positions_path = vehicles_meta["path"]
        ctx.upload(positions_path, positions_path)

    summary_path = f"data/summaries/{date}.json"
    ctx.upload(summary_path, summary_path)
