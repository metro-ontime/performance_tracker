from pandas import read_csv

class Calendar:
    def __init__(self, path):
        self.all = parse_dates(read_csv(path))
        self.today = filter_for_today(self.all)

def parse_dates(calendar):
    calendar.start_date = calendar.start_date.apply(lambda row: str(row)[4:6] + '/' + str(row)[6:8] + '/' + str(row)[0:4])
    calendar.end_date = calendar.end_date.apply(lambda row: str(row)[4:6] + '/' + str(row)[6:8] + '/' + str(row)[0:4])
    calendar.start_date = pd.to_datetime(calendar['start_date'])
    calendar.end_date = pd.to_datetime(calendar['end_date'])
    return calendar

def filter_for_today(calendar):
    mask = (calendar['end_date'] >= today)
    calendar = calendar[mask]
    mask = (calendar['start_date'] <= today)
    calendar = calendar[mask]
    return calendar
