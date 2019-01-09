from helpers.upload import upload


# date = pendulum.now("UTC").start_of("day")
# date_formatted = date.format("YYYY-MM-DD")
date_formatted = "2018-12-31"
agency = "lametro-rail"

for line in range(801, 807):
    source_path = f"data/schedule/{line}_{agency}/{date_formatted}.csv"
    upload(source_path, source_path)
