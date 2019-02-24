import pendulum
import os
import pandas as pd
from .datetimefs import DateTimeFS


def check_datetime(datetime, dates, formatting):
    if not dates:
        raise Exception("Dates array empty")
    if datetime.format(formatting) in dates:
        return True
    return False


def get_schedule_path(datetime, base_path):
    yyyy_mm_dd = datetime.format("YYYY-MM-DD")
    schedule_path = os.path.join(base_path, f"{yyyy_mm_dd}.csv")
    return schedule_path


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


def get_appropriate_schedule(datetime, base_path):
    datetime = datetime.in_tz("America/Los_Angeles")
    schedule_datetime = get_date_if_exists_otherwise_previous(datetime, base_path)

    schedule_path = get_schedule_path(schedule_datetime, base_path)
    schedule_on_this_date = pd.read_csv(schedule_path)
    schedule_start = first_scheduled_arrival(schedule_on_this_date)
    schedule_end = last_scheduled_arrival(schedule_on_this_date)

    if datetime < schedule_start:
        schedule_datetime = schedule_datetime.subtract(days=1)
        schedule_path = get_schedule_path(schedule_datetime, base_path)
        schedule_on_this_date = pd.read_csv(schedule_path)
        schedule_start = first_scheduled_arrival(schedule_on_this_date)
        schedule_end = last_scheduled_arrival(schedule_on_this_date)

    return {"path": schedule_path, "start": schedule_start, "end": schedule_end}


def first_scheduled_arrival(schedule):
    return pendulum.parse(schedule.datetime.min(), tz="America/Los_Angeles")


def last_scheduled_arrival(schedule):
    return pendulum.parse(schedule.datetime.max(), tz="America/Los_Angeles")
