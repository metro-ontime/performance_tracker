import os
import pendulum
import pandas as pd
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
trips_and_directions = trips_running_today[['trip_id', 'direction_id']]

for line_no in range(801, 807):
    line_trips = trips_running_today[trips_running_today["route_id"] == line_no]
    line_schedule = full_schedule[full_schedule["trip_id"].isin(line_trips["trip_id"])]
    line_schedule = scheduleTimeToDateTime(line_schedule, start_date)
    line_schedule = pd.merge(line_schedule, trips_and_directions, on="trip_id")
    os.makedirs(f"data/schedule/{line_no}_{agency}", exist_ok=True)
    path = f"data/schedule/{line_no}_{agency}/{start_date}.csv"
    line_schedule.to_csv(path)
