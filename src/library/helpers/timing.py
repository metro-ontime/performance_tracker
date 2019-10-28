import pendulum
import os
import pandas as pd
from .datetimefs import DateTimeFS


def check_datetime(datetime, dates, formatting):
    if not dates:
        raise Exception("Dates array empty")
    if datetime.format(formatting) in dates:
        print('date is present!')
        return True
    print('date not present')
    return False


def format_date_path(datetime, base_path):
    yyyy_mm_dd = datetime.format("YYYY-MM-DD")
    return os.path.join(base_path, f"{yyyy_mm_dd}.csv")


def get_date_if_exists_otherwise_previous(datetime, base_path):
    dtfs = DateTimeFS(base_path)
    available_dates = dtfs.get_all_dates(tz="America/Los_Angeles")
    formatted_dates = [date.format("YYYY-MM-DD") for date in available_dates]
    try:
        if check_datetime(datetime, formatted_dates, "YYYY-MM-DD"):
            return datetime
        elif check_datetime(datetime.subtract(days=1), formatted_dates, "YYYY-MM-DD"):
            return datetime.subtract(days=1)
        return None
    except:
        return None


def get_appropriate_timetable(datetime, base_path):
    datetime = datetime.in_tz("America/Los_Angeles")
    file_datetime = get_date_if_exists_otherwise_previous(datetime, base_path)
    path = format_date_path(file_datetime, base_path)
    df = pd.read_csv(path, index_col=0)
    start = first_entry(df)
    end = last_entry(df)
    if datetime < start:
        file_datetime = file_datetime.subtract(days=1)
        path = format_date_path(file_datetime, base_path)
        df = pd.read_csv(path, index_col=0)
        start = first_entry(df)
        end = last_entry(df)

    return {
        "path": path,
        "start": start,
        "end": end,
        "data": df,
        "date": file_datetime.format("YYYY-MM-DD"),
    }


def first_entry(schedule):
    return pendulum.parse(schedule.datetime.min(), tz="America/Los_Angeles")


def last_entry(schedule):
    return pendulum.parse(schedule.datetime.max(), tz="America/Los_Angeles")
