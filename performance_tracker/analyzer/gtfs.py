import json
from pandas import read_csv
from .schedule import Schedule
from .line import Line
from .tracker import selectAnalysisWindow
from .calendar import Calendar
from .trips import Trips

def load_and_parse_schedule(date, timemin, timemax):
    today = date
    start_datetime = today + ' ' + timemin
    end_datetime = today + ' ' + timemax

    track = json.load(open('data/GTFS/goldJSON.json'))
    stations = json.load(open('data/GTFS/GoldLineStationIds.json'))['items']
    full_schedule = read_csv('data/GTFS/stop_times.txt')

    calendar = Calendar('data/GTFS/calendar.txt')
    services_running_today = list(calendar.on_date(today).service_id)
    trips = Trips('data/GTFS/trips.txt')
    trips_running_today = trips.filter_by_service_id(services_running_today)

    gold_schedule_today = Schedule(today, '804', full_schedule, trips_running_today)
    gold_line = Line(804, track, stations, gold_schedule_today)

    return selectAnalysisWindow(gold_line.getScheduleWithCoordinates(), start_datetime, end_datetime)
