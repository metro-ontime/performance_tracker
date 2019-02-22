import pendulum
import os
import pandas as pd


def get_latest_schedule(line, agency, datetime, base_path):
    datetime = datetime.in_timezone("America/Los_Angeles")
    yyyy_mm_dd = datetime.format("YYYY-MM-DD")
    schedule_path = os.path.join(base_path, f"{line}_{agency}/{yyyy_mm_dd}.csv")

    while not os.path.exists(schedule_path):
        datetime = datetime.subtract(days=1)
        yyyy_mm_dd = datetime.format("YYYY-MM-DD")
        schedule_path = os.path.join(base_path, f"{line}_{agency}/{yyyy_mm_dd}.csv")
    return schedule_path


def get_appropriate_schedule(line, agency, datetime, base_path):
    schedule_path = get_latest_schedule(line, agency, datetime, base_path)
    if datetime < first_scheduled_arrival(schedule_path):
        datetime = datetime.subtract(days=1)
        schedule_path = get_latest_schedule(line, agency, datetime, base_path)
    return schedule_path


def first_scheduled_arrival(schedule_path):
    schedule_on_this_date = pd.read_csv(schedule_path)
    return pendulum.parse(
        schedule_on_this_date.datetime.min(), tz="America/Los_Angeles"
    )


def last_scheduled_arrival(schedule_path):
    schedule_on_this_date = pd.read_csv(schedule_path)
    return pendulum.parse(
        schedule_on_this_date.datetime.max(), tz="America/Los_Angeles"
    )
