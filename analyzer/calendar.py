from pandas import read_csv, to_datetime

class Calendar:
    def __init__(self, path):
        self.all = parse_dates(read_csv(path))

    def on_date(self, date_string):
        today = to_datetime(date_string)
        mask = (self.all['end_date'] >= today)
        calendar = self.all[mask]
        mask = (calendar['start_date'] <= today)
        calendar = calendar[mask]
        return calendar

def parse_dates(calendar):
    calendar.start_date = calendar.start_date.apply(lambda row: str(row)[4:6] + '/' + str(row)[6:8] + '/' + str(row)[0:4])
    calendar.end_date = calendar.end_date.apply(lambda row: str(row)[4:6] + '/' + str(row)[6:8] + '/' + str(row)[0:4])
    calendar.start_date = to_datetime(calendar['start_date'])
    calendar.end_date = to_datetime(calendar['end_date'])
    return calendar

