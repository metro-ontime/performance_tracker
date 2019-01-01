import pandas as pd
from datetime import timedelta


def scheduleTimeToDateTime(schedule, date):
    schedule["arrival_hour"] = schedule.arrival_time.apply(
        lambda row: int(str(row)[0:2])
    )
    schedule["arrival_min"] = schedule.arrival_time.apply(
        lambda row: int(str(row)[3:5])
    )

    today = schedule[schedule["arrival_hour"] < 24]
    tomorrow = schedule[schedule["arrival_hour"] >= 24]

    today["datetime"] = today.apply(
        lambda row: makeDateTime(date, row["arrival_time"]), axis=1
    )
    tomorrow["datetime"] = tomorrow.apply(
        lambda row: makeTomorrowDateTime(date, row["arrival_hour"], row["arrival_min"]),
        axis=1,
    )

    schedule = pd.concat([today, tomorrow])
    return schedule


def hourMinusDay(hour):
    new_hour = int(hour) - 24
    return "{0:0=2d}".format(new_hour)


def makeDateTime(date, time):
    return pd.to_datetime(date + " " + time)


def makeTomorrowDateTime(date, hour, minute):
    return pd.to_datetime(
        date + " " + hourMinusDay(hour) + ":" + str(minute) + ":00"
    ) + timedelta(days=1)
