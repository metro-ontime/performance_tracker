import json
from pandas import read_csv
from .schedule import Schedule
from .line import Line
from .tracker import selectAnalysisWindow
from .calendar import Calendar
from .trips import Trips


def load_and_parse_schedule(line_no, start_datetime, end_datetime):
    start_date = start_datetime.format("YYYY-MM-DD")
    end_date = end_datetime.format("YYYY-MM-DD")
    full_schedule = read_csv("data/GTFS/stop_times.txt")
    calendar = Calendar("data/GTFS/calendar.txt")
    trips = Trips("data/GTFS/trips.txt")
    services_running_today = calendar.services_running_on(start_date)
    trips_running_today = trips.filter_by_service_id(services_running_today)

    track = load_track(line_no)
    stations = load_station_names(line_no)
    schedule_today = Schedule(start_date, line_no, full_schedule, trips_running_today)
    line = Line(line_no, track, stations, schedule_today)

    return selectAnalysisWindow(line.getScheduleWithCoordinates(), start_date, end_date)


def load_track(line_no):
    with open(f"data/line_info/{line_no}/shape.json") as track_data:
        track = json.load(track_data)
    return track


def load_station_names(line_no):
    with open(f"data/line_info/{line_no}/stations.json") as station_data:
        names = json.load(station_data)["items"]
    return names
