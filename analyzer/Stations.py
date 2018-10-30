from .geoHelpers import toGDF, findRelativePositions
from pandas import Series

def prepareStations(stations, track):
    stations = toGDF(stations)
    stations = findRelativePositions(stations, track)
    stations = splitStopIds(stations, 'id')
    return stations

def split_stop_ids(stationList, id_field):
    line_ids = list(map(lambda x: str(x)[0:3], list(stationList[id_field])))
    station_ids = list(map(lambda x: str(int(str(x)[3:5])), list(stationList[id_field])))
    stationList.loc[:, 'line_id'] = Series(line_ids, index=stationList.index)
    stationList.loc[:, 'station_id'] = Series(station_ids, index=stationList.index)
    return stationList

  

