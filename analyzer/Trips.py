from pandas import read_csv

class Trips:
    def __init__(self, path):
        self.all = read_csv(path)

    def filter_by_service_id(self, service_ids):
        trips = self.all
        trips.loc[:, 'today'] = trips.service_id.apply(lambda service: service in service_ids)
        trips = trips[trips.today == True]
        return list(trips.trip_id)
