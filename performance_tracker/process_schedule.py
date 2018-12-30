import os
import pendulum
from pandas import read_csv
from analyzer.calendar import Calendar
from analyzer.trips import Trips
from analyzer.schedule import Schedule

start_datetime = pendulum.today("America/Los_Angeles")
start_date = start_datetime.format("YYYY-MM-DD")
agency = "lametro-rail"

full_schedule = read_csv("data/GTFS/stop_times.txt")
calendar = Calendar("data/GTFS/calendar.txt")
trips = Trips("data/GTFS/trips.txt")
services_running_today = calendar.services_running_on(start_date)
trips_running_today = trips.filter_by_service_id(services_running_today)

for line_no in range(801, 805):
    os.makedirs(f"data/schedule/{line_no}_{agency}", exist_ok=True)
    schedule_today = Schedule(start_date, line_no, full_schedule, trips_running_today)
    path = f"data/schedule/{line_no}_{agency}/{start_date}.csv"
    schedule_today.times.to_csv(path)
