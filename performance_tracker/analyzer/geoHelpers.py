import pandas as pd
import geopandas as gpd
from shapely.geometry import Point


def findRelativePositions(positions, line):
    relative_positions = [
        line.project(position.geometry) / line.length
        for index, position in positions.iterrows()
    ]
    return pd.Series(relative_positions, index=positions.index)


def toGDF(data):
    data = pd.DataFrame(data)
    data = gpd.GeoDataFrame(
        data, geometry=[Point(xy) for xy in zip(data.longitude, data.latitude)]
    )
    data = data.drop(["latitude", "longitude"], axis=1)
    return data
