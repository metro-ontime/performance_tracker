class Table:
    def __init__(self, agency, line):
        self.agency = agency
        self.line = line

    def create(self):
        agency = self.agency
        line = self.line
        return f"CREATE TABLE IF NOT EXISTS {agency}_{line} (id INTEGER PRIMARY KEY AUTOINCREMENT, query_time DATETIME NOT NULL, seconds_since_report INTEGER NOT NULL, vehicle_id INTEGER NOT NULL, latitude REAL NOT NULL, longitude REAL NOT NULL, direction REAL NOT NULL)"

    def insert(self):
        line = self.line
        agency = self.agency
        return f"INSERT INTO {agency}_{line} (query_time, seconds_since_report, vehicle_id, latitude, longitude, direction) VALUES (?, ?, ?, ?, ?, ?)"

    def all_fields_present(self, obj):
        necessary_fields = ['id', 'seconds_since_report', 'latitude', 'longitude', 'direction']
        if all (key in obj for key in necessary_fields):
            return True
        return False
