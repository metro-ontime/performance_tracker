from shapely.geometry import Point
import geopandas as gpd
import pandas as pd
from datetime import timedelta
from .geoHelpers import findRelativePositions


def getTrips(log):
    # TODO: We should revise how this works
    # It might be better to use a dict of vehicles to keep track of direction, trip_id and position
    # then increment a counter every time direction changes or position goes backwards
    # That way we only need to sort by datetime
    vehicles = log.sort_values(["vehicle_id", "datetime"])
    vehicles.loc[:, "trip_id"] = 0
    trip_id = 0
    previous_direction = 0
    previous_vehicle = 0
    previous_position = 0
    for index, row in vehicles.iterrows():
        if (
            row.direction != previous_direction
            or row.vehicle_id != previous_vehicle
            or row.relative_position < previous_position
        ):
            trip_id += 1
        previous_direction = row.direction
        previous_vehicle = row.vehicle_id
        previous_position = row.relative_position
        vehicles.loc[index, "trip_id"] = trip_id
    return vehicles
