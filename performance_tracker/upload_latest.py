from helpers.upload import upload
import pendulum


date = pendulum.today("America/Los_Angeles")
date_formatted = date.format("YYYY-MM-DD")
agency = "lametro-rail"

for line in range(801, 807):
    summary_path = f"data/summaries/{line}_{agency}/{date_formatted}.json"
    positions_path = (
        f"data/vehicle_tracking/processed/{line}_{agency}/{date_formatted}.csv"
    )
    upload(summary_path, summary_path)
    upload(positions_path, positions_path)
