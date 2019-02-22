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


def bullshit():
    first_scheduled_arrival = pendulum.parse()
    if now < first_scheduled_arrival:
        # i.e. if now is earlier than the first scheduled train on this date,
        # we must be still on yesterday's timetable
        schedule_yesterday = pd.read_csv(
            f"data/schedule/{line}_{agency}/{yesterday}.csv"
        )
        start_datetime = pendulum.parse(
            schedule_yesterday.datetime.min(), tz="America/Los_Angeles"
        )
    else:
        start_datetime = first_scheduled_arrival

    path_base = f"data/vehicle_tracking/raw/{line}_{agency}"

    dtfs = DateTimeFS(path_base)

    datetimes = dtfs.get_datetimes_in_range(
        start_datetime.in_tz("UTC"), end_datetime.in_tz("UTC")
    )
