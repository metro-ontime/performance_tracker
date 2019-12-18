import pendulum
import os
import pandas as pd


def get_appropriate_timetable(datetime, base_path, ctx):
    datestring = datetime.in_tz(ctx.config["TIMEZONE"]).format("YYYY-MM-DD")
    path = os.path.join(base_path, f"{datestring}.csv")
    try:
        # Try load schedule for today
        df = pd.read_csv(path, index_col=0, parse_dates=["datetime"])
    except:
        # If today's schedule not found, we try to find yesterday's
        ctx.logger(f"Could not find data at {path}")
        datestring = datetime.in_tz(ctx.config["TIMEZONE"]).subtract(days=1).format("YYYY-MM-DD")
        path = os.path.join(base_path, f"{datestring}.csv")
        ctx.logger(f"Trying {path} instead...")
        try:
            df = pd.read_csv(path, index_col=0, parse_dates=["datetime"])
        except:
            # If yesterday's schedule not found, give up
            raise Exception(f"Could not find data at {path}")

    start = pandas_datetime_to_pendulum_datetime(df.datetime.min(), ctx.config["TIMEZONE"])
    ctx.logger(start)
    if datetime < start:
        # This occurs when we have the new schedule for the day,
        # but the current datetime is earlier than the first scheduled service.
        # In this case we assume we are still on yesterday's schedule.
        datestring = datetime.in_tz(ctx.config["TIMEZONE"]).subtract(days=1).format("YYYY-MM-DD")
        path = os.path.join(base_path, f"{datestring}.csv")
        try:
            df = pd.read_csv(path, index_col=0, parse_dates=["datetime"])
        except:
            # If yesterday's schedule not found, give up
            raise Exception(f"Could not find data at {path}")
    return df

def pandas_datetime_to_pendulum_datetime(pd_datetime, tz):
    return pendulum.parse(pd_datetime.strftime('%Y-%m-%dT%H:%M:%S%z'), tz=tz)
