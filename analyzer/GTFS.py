import json
from pandas import read_csv
from .Schedule import Schedule
from .Line import Line
from .Tracker import selectAnalysisWindow
from .Calendar import Calendar
from .Trips import Trips

def parse(date, timemin, timemax):
    today = date
    start_datetime = today + ' ' + timemin
    end_datetime = today + ' ' + timemax

    track = json.load(open('shapefiles/gold_northbound/goldJSON.json'))
    stations = json.load(open('misc/GoldLineStationIds.json'))['items']
    full_schedule = read_csv('GTFS/stop_times.txt')

    calendar = Calendar('GTFS/calendar.txt'):
    services_running_today = list(calendar.on_date(today).service_id)
    trips = Trips('GTFS/trips.txt')
    trips_running_today = trips.filter_by_service_id(services_running_today)

    gold_schedule_today = Schedule(today, '804', full_schedule, trips_running_today)
    gold_line = Line(804, track, stations, gold_schedule_today)

    return selectAnalysisWindow(gold_line.getScheduleWithCoordinates(), start_datetime, end_datetime)
