import os
import pendulum
from pandas import read_csv
from .calendar import Calendar
from .trips import Trips
from .schedule import Schedule

start_datetime = pendulum.today("America/Los_Angeles")
start_date = start_datetime.format("YYYY-MM-DD")
agency = "lametro-rail"
datestring = start_datetime.format("YYYY-MM-DD")

full_schedule = read_csv("data/GTFS/stop_times.txt")
calendar = Calendar("data/GTFS/calendar.txt")
trips = Trips("data/GTFS/trips.txt")
services_running_today = calendar.services_running_on(start_date)
trips_running_today = trips.filter_by_service_id(services_running_today)

# TO DO: Once all line data (shapefiles) are prepared,
# change range to cover all lines
for line_no in range(804, 805):
    os.makedirs(f"data/schedule/{line_no}_{agency}", exist_ok=True)
    schedule_today = Schedule(start_date, line_no, full_schedule, trips_running_today)
    path = f"data/schedule/{line_no}_{agency}/{datestring}.csv"
    schedule_today.to_csv(path)
