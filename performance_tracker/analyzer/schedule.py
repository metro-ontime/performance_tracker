import pandas as pd
import pendulum
from datetime import timedelta


def scheduleTimeToDateTime(schedule, date):
    """
    schedule: pandas dataframe input with "arrival_hour", "arrival_min" fields.
    date: Date formatted YYYY-MM-DD. This is the date we will assign the arrival times to when constructing timestamps.
    Metro schedule times are given in an unconventional 27hr clock format. All times are relative to 00:00 (midnight) of the timetable day they are assigned to. Some times (i.e. >23:59) are assigned to the previous calendar day because they are the very late services running past midnight. We have to convert all these given times to conventional ISO8601 timestamps before we can use them.
    """
    schedule["arrival_hour"] = schedule.arrival_time.apply(
        lambda row: int(str(row)[0:2])
    )
    schedule["arrival_min"] = schedule.arrival_time.apply(
        lambda row: int(str(row)[3:5])
    )

    today = schedule[schedule["arrival_hour"] < 24]
    tomorrow = schedule[schedule["arrival_hour"] >= 24]

    today["datetime"] = today.apply(
        lambda row: makeDateTime(date, row["arrival_time"]).to_iso8601_string(), axis=1
    )
    tomorrow["datetime"] = tomorrow.apply(
        lambda row: makeDateTime(
            date,
            f"{'{0:0=2d}'.format(row['arrival_hour'] - 24)}:{'{0:0=2d}'.format(row['arrival_min'])}:00",
        )
        .add(days=1)
        .to_iso8601_string(),
        axis=1,
    )

    schedule = pd.concat([today, tomorrow])
    schedule = schedule.drop(["arrival_hour", "arrival_min"], axis=1)
    return schedule


def makeDateTime(date, time):
    return pendulum.parse(f"{date}T{time}", tz="America/Los_Angeles")
