import pendulum
from library.helpers.timing import get_appropriate_timetable
import os

def upload_latest(ctx, dt):
    agency = ctx.config["METRO_AGENCY"]

    for line in range(801, 807):
        vehicles_base_path = f"data/tmp/tracking/{agency}/{line}/processed"
        vehicles_meta = get_appropriate_timetable(dt, vehicles_base_path)
        date = vehicles_meta["date"]
        positions_path = vehicles_meta["path"]
        ctx.datastore.upload(f"tracking/{agency}/{line}" , positions_path),

    summary_path = os.path.join(os.getcwd() , f"data/summaries/{agency}/{date}.json")
    ctx.datastore.upload(f"summaries/{agency}/{date}.json" , summary_path)
    
    return 0