import os
import pendulum
from pandas import read_csv
from analyzer.calendar import Calendar
from analyzer.schedule import scheduleTimeToDateTime

start_datetime = pendulum.today("America/Los_Angeles")
start_date = start_datetime.format("YYYY-MM-DD")
agency = "lametro-rail"

# Load all data
full_schedule = read_csv("data/GTFS/stop_times.txt")
calendar = Calendar("data/GTFS/calendar.txt")
trips = read_csv("data/GTFS/trips.txt")

# pre-processing (operations on full datasets)
services_running_today = calendar.services_running_on(start_date).service_id
trips_running_today = trips[trips["service_id"].isin(services_running_today)]

for line_no in range(801, 807):
    line_trips = trips_running_today[trips_running_today["route_id"] == line_no]
    line_schedule = full_schedule[full_schedule["trip_id"].isin(line_trips["trip_id"])]
    with_corrected_times = scheduleTimeToDateTime(line_schedule, start_date)
    os.makedirs(f"data/schedule/{line_no}_{agency}", exist_ok=True)
    path = f"data/schedule/{line_no}_{agency}/{start_date}.csv"
    with_corrected_times.to_csv(path)
