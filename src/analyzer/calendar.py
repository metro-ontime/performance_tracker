import pendulum
import pandas as pd


class Calendar:
    def __init__(self, path):
        self.all = parse_dates(pd.read_csv(path))

    def services_running_on(self, datestring):
        within_range = self.on_date(datestring)
        date = pendulum.from_format(datestring, "YYYY-MM-DD")
        day = date.format("dddd").lower()
        return within_range[within_range[day] == 1]

    def on_date(self, date):
        today = pd.to_datetime(date)
        mask = self.all["end_date"] >= today
        calendar = self.all[mask]
        mask = calendar["start_date"] <= today
        calendar = calendar[mask]
        return calendar


def parse_dates(calendar):
    calendar.start_date = calendar.start_date.apply(
        lambda row: pd.to_datetime(
            pendulum.from_format(str(row), "YYYYMMDD").format("YYYY-MM-DD")
        )
    )
    calendar.end_date = calendar.end_date.apply(
        lambda row: pd.to_datetime(
            pendulum.from_format(str(row), "YYYYMMDD").format("YYYY-MM-DD")
        )
    )
    return calendar
