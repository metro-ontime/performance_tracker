from shapely.geometry import Point
from App.classes.geoHelpers import findRelativePositions
import geopandas as gpd
import pandas as pd

def rawLogToGDF(log):
    #log['datetime'] = pd.to_datetime(log['report_date'] + ' ' + log['report_time'])
    log = log.drop_duplicates(subset=['datetime', 'lat', 'lon', 'vehicle_id'])
    #log = log.drop(['report_date', 'report_time', 'id'], axis=1)
    geometry = [Point(xy) for xy in zip(log.lon, log.lat)]
    return gpd.GeoDataFrame(log, crs = {'init': 'epsg:4326'}, geometry = geometry)
  
def selectAnalysisWindow(log, start_date, end_date):
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    mask = (log['datetime'] >= start_date) & (log['datetime'] <= end_date)
    return log.loc[mask]

def analyzeSelection(log, stations, line):
    log = findRelativePositions(log, line)
    log = getSurroundingStops(log, stations)
    log = getTrips(log)
    return log

def getTrips(log):
    vehicles = log.sort_values(['vehicle_id', 'datetime'])
    trip_id = 0
    previous_direction = 0
    previous_vehicle = 0
    for index, position in vehicles.iterrows():
        if position.direction != previous_direction or position.vehicle_id != previous_vehicle:
            trip_id += 1
        previous_direction = position.direction
        previous_vehicle = position.vehicle_id
        vehicles.loc[index, 'trip_id'] = trip_id
    return vehicles

def getSurroundingStops(log, stations):
    for index, train in log.iterrows():
        surrounding_stops = find_surrounding_stops(train.relative_position, train.direction, stations)
        previous_stop = surrounding_stops[0]
        next_stop = surrounding_stops[1]
        log.loc[index, 'previous_stop'] = previous_stop['display_name']
        log.loc[index, 'next_stop'] = next_stop['display_name']
    return log

def find_surrounding_stops(relative_pos_of_train, direction, stations):
    reverse = direction / 180
    next_stop = None
    previous_stop = None
    for index, station in stations.iterrows():        
        if relative_pos_of_train < station.relative_position:
            next_stop = stations.loc[max(index - reverse, 0)]
            previous_stop = stations.loc[max(index - 1 + reverse, 0)]
            break
    if (next_stop is None):
        next_stop = {"display_name": "EOL"}
    if (previous_stop is None):
        previous_stop = {"display_name": "EOL"}
    return [previous_stop, next_stop]
          