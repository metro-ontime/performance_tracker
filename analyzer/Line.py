from .Track import create_ordered_line
from .Stations import prepareStations
import pandas as pd

class Line:
    def __init__(self, line_id, track, stations, schedule):
        self.id = str(line_id)
        self.track = create_ordered_line(track)
        self.stations = prepareStations(stations, self.track)
        self.schedule = schedule

    def getScheduleWithCoordinates(self):
        merged = self.schedule.times.merge(self.stations, how = 'inner', on = 'station_id')
        return merged[['datetime', 'trip_id', 'arrival_time', 'departure_time', 'stop_id', 'station_id', 'display_name', 'stop_headsign', 'relative_position', 'geometry']]

