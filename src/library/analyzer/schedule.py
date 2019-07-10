import pandas as pd
import pendulum
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
