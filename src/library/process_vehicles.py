import pandas as pd
from library.analyzer.process_vehicles import (
    get_track,
    process_raw_vehicles
)

def process_vehicles(ctx, datetime):
    agency = ctx.config["METRO_AGENCY"]
    lines = ctx.config["METRO_LINES"]
    ctx.logger("Processing vehicle observations for all lines")

    for line in lines:
        # - grab the currently applicable schedule
        schedule_base_path = f"schedule/{agency}/{line}"
        try:
            schedule = get_appropriate_timetable(datetime, schedule_base_path, ctx)
            date = pandas_datetime_to_pendulum_datetime(schedule.datetime.min(), ctx.config["TIMEZONE"]).format("YYYY-MM-DD")
        except:
            # In the case that no schedule is available,
            # we revert to following the regular 24hr clock
            date = datetime.in_tz(ctx.config["TIMEZONE"]).format("YYYY-MM-DD")

        # grab preprocessed data
        preprocessed_path = ctx.datastore.get_abs_path(f"tracking/preprocessed/{agency}/{line}/{date}.csv")
        try:
            data = pd.read_csv(preprocessed_path, index_col=0)
        except:
            ctx.logger("Could not get preprocessed data for line {line}")
            continue

        # get track data for line
        try:
            tracks = get_track(line, ctx.config["LOCAL_DATA"])
        except Exception as e:
            ctx.logger(f"Could not get track data for line {line}")
            ctx.logger(e)
            continue

        # do processing
        try:
            processed = process_raw_vehicles(data, tracks)
        except Exception as e:
            ctx.logger(f"Could not process observations for line {line}")
            ctx.logger(e)
            continue

        ctx.logger(f"Saving processed vehicle data for line {line} and date {date}")
        ctx.datastore.write(f"tracking/processed/{agency}/{line}/{date}.csv", processed.to_csv())
    return 0
