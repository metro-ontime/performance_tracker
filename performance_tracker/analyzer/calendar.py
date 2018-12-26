import pendulum
from pandas import read_csv, to_datetime


class Calendar:
    def __init__(self, path):
        self.all = parse_dates(read_csv(path))

    def services_running_on(self, date):
        return list(self.on_date(date).service_id)

    def on_date(self, date):
        today = to_datetime(date)
        mask = self.all["end_date"] >= today
        calendar = self.all[mask]
        mask = calendar["start_date"] <= today
        calendar = calendar[mask]
        return calendar


def parse_dates(calendar):
    calendar.start_date = calendar.start_date.apply(
        lambda row: to_datetime(
            pendulum.from_format(str(row), "YYYYMMDD").format("YYYY-MM-DD")
        )
    )
    calendar.end_date = calendar.end_date.apply(
        lambda row: to_datetime(
            pendulum.from_format(str(row), "YYYYMMDD").format("YYYY-MM-DD")
        )
    )
    return calendar
