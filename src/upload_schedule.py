from helpers.upload import upload
import pendulum


date = pendulum.today("America/Los_Angeles")
date_formatted = date.format("YYYY-MM-DD")
agency = "lametro-rail"

for line in range(801, 807):
    source_path = f"data/schedule/{line}_{agency}/{date_formatted}.csv"
    upload(source_path, source_path)
