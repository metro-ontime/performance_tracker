import pandas as pd
from library.analysis.nextbus import parse_nextbus_response

from library.get_vehicles import get_vehicles_for_line
from library.helpers.timing import get_appropriate_timetable, pandas_datetime_to_pendulum_datetime

def record(ctx, datetime):
    agency = ctx.config["METRO_AGENCY"]
    lines = ctx.config["METRO_LINES"]
    base_url = ctx.config["VEHICLE_API_URL"]

    latest_observations = { line:get_vehicles_for_line(base_url, agency, line) for line in lines }

    for line in lines:
        # - grab the new JSON response from the API
        line_observations = latest_observations[line]

        # - grab the currently applicable schedule
        schedule_base_path = ctx.datastore.get_abs_path(f"schedule/{agency}/{line}")
        try:
            schedule = get_appropriate_timetable(datetime, schedule_base_path, ctx)
            start = pandas_datetime_to_pendulum_datetime(schedule.datetime.min(), ctx.config["TIMEZONE"]).format("YYYY-MM-DD")
        except:
            # In the case that no schedule is available,
            # we revert to following the regular 24hr clock
            start = datetime.in_tz(ctx.config["TIMEZONE"]).format("YYYY-MM-DD")

        # - grab the running list of tracked vehicle positions for this schedule period
        preprocessed_path = ctx.datastore.get_abs_path(f"tracking/preprocessed/{agency}/{line}/{start}.csv")
        try:
            df = pd.read_csv(preprocessed_path, index_col=0)
        except:
            df = pd.DataFrame(columns=["line", "vehicle_id","direction","report_time","latitude","longitude","predictable"])

        # - append the new JSON to the running list
        try:
            latest = parse_nextbus_response(line_observations)
        except Exception as exc:
            ctx.logger(f"Error parsing vehicle JSON for line {line}: {exc}")
            continue
        df = pd.concat([df, latest], ignore_index=True, sort=False, join="inner")

        # - Run basic data cleanup
        df = df.dropna()

        # - write the running list to disk
        ctx.datastore.write(preprocessed_path, df.to_csv())

    return 0
