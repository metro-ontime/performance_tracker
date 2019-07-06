import pandas as pd
import geopandas as gpd
from shapely.geometry import Point


def findRelativePositions(positions, line):
    # TODO: Add caching by using a dictionary with tuples (coordinates) as keys
    return positions.geometry.apply(lambda xy: line.project(xy) / line.length)


def toGDF(data):
    data = pd.DataFrame(data)
    data = gpd.GeoDataFrame(
        data, geometry=[Point(xy) for xy in zip(data.longitude, data.latitude)]
    )
    data = data.drop(["latitude", "longitude"], axis=1)
    return data
