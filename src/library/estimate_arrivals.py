import os
import pandas as pd

from library.analyzer.estimate_arrivals import estimate_arrivals_by_trip
from library.analyzer.analyze_estimates import (
    match_arrivals_with_schedule,
    match_previous_stop_times,
)
from library.helpers.timing import get_appropriate_timetable, pandas_datetime_to_pendulum_datetime
from library.analyzer.summary import statistic_summary


def estimate_arrivals(ctx ,datetime):
    agency = ctx.config["METRO_AGENCY"]
    lines = ctx.config["METRO_LINES"]
    ctx.logger("Estimating station arrivals and generating summary stats for all lines")
    master_summary = {}

    for line in lines:
        schedule_base_path = f"schedule/{agency}/{line}"
        try:
            schedule = get_appropriate_timetable(datetime, schedule_base_path, ctx)
        except Exception as exc:
            ctx.logger(exc)
            ctx.logger(f"Couldn't get schedule data for line {line}")
            continue
        vehicles_base_path = f"tracking/processed/{agency}/{line}"
        try:
            vehicles = get_appropriate_timetable(datetime, vehicles_base_path, ctx)
        except Exception as exc:
            ctx.logger(exc)
            ctx.logger(f"Couldn't get vehicle data for line {line}")
            continue

        first_schedule_date = pandas_datetime_to_pendulum_datetime(schedule.datetime.min(), ctx.config["TIMEZONE"]).format("YYYY-MM-DD")
        first_vehicles_date = pandas_datetime_to_pendulum_datetime(vehicles.datetime.min(), ctx.config["TIMEZONE"]).format("YYYY-MM-DD")

        if not first_schedule_date == first_vehicles_date:
            ctx.logger(f"Schedule date does not match tracked vehicle data for line {line}")
            ctx.logger(f"Schedule date: {first_schedule_date}")
            ctx.logger(f"Tracking data date: {first_vehicles_date}")
            continue

        try:
            all_estimates = list()
            for direction in range(2):
                vehicles_direction = vehicles[vehicles["direction_id"] == direction]
                schedule_direction = schedule[schedule["direction_id"] == direction]
                stations = pd.read_csv(
                    os.path.join(
                        ctx.config["LOCAL_DATA"],
                        f"line_info/{line}/{line}_{direction}_stations.csv"
                    ),
                    index_col=0
                )
                trips = vehicles_direction.groupby(["trip_id"])

                ctx.logger(f"Beginning heavy calculations for line {line} and direction {direction}")
                ### Heavy calculations
                estimates = estimate_arrivals_by_trip(trips, stations, direction)
                ctx.logger("Finished estimating arrivals by trip")
                estimates = match_arrivals_with_schedule(estimates, schedule_direction)
                ctx.logger("Finished matching arrivals with schedule")
                estimates = match_previous_stop_times(estimates)
                ctx.logger("Finished matching previous stop times")
                ###
                ctx.logger(f"Completed heavy calculations for line {line} and direction {direction}")

                # append this set of estimates to list
                all_estimates.append(estimates)
            # concat estimates into 1 df
            all_estimates = pd.concat(all_estimates)[
                [
                    "datetime",
                    "stop_id",
                    "direction_id",
                    "closest_scheduled",
                    "since_prev_stop",
                    "since_scheduled",
                ]
            ]

            master_summary[f"{line}_{agency}"] = statistic_summary(
                all_estimates, schedule, first_schedule_date, datetime.to_iso8601_string()
            )
        except Exception as e:
            ctx.logger(f"Estimating arrival times and/or matching with schedule failed for line {line}")
            ctx.logger(e)
            continue

    # write master summary
    ctx.logger("Saving all summary data")
    ctx.datastore.write_json(f"summaries/{agency}/{first_schedule_date}.json", master_summary)
    return 0
