from App.classes.geoHelpers import toGDF, findRelativePositions
import pandas as pd

def prepareStations(stations, track):
    stations = toGDF(stations)
    stations = findRelativePositions(stations, track)
    stations = splitStopIds(stations, 'id')
    return stations

def splitStopIds(stationList, id_field):
    line_ids = list(map(lambda x: str(x)[0:3], list(stationList[id_field])))
    station_ids = list(map(lambda x: str(int(str(x)[3:5])), list(stationList[id_field])))
    stationList.loc[:, 'line_id'] = pd.Series(line_ids, index=stationList.index)
    stationList.loc[:, 'station_id'] = pd.Series(station_ids, index=stationList.index)
    #stationList = stationList.rename(columns={id_field: 'stop_id_original'})
    return stationList

  

