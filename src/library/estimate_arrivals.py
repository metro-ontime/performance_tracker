import pandas as pd
from library.analyzer.estimate_arrivals import estimate_arrivals_by_trip
from library.analyzer.analyze_estimates import (
    match_arrivals_with_schedule,
    match_previous_stop_times,
)

def estimate_arrivals(ctx ,datetime):
    from library.helpers.timing import get_appropriate_timetable
    from library.analyzer.summary import statistic_summary

    agency = ctx.config["METRO_AGENCY"]

    master_summary = {}

    for line in range(801, 807):
        schedule_base_path = ctx.datastore.get_abs_path(f"schedule/{agency}/{line}")
        schedule_metadata = get_appropriate_timetable(datetime, schedule_base_path)
        vehicles_base_path = ctx.datastore.get_abs_path(f"tracking/{agency}/{line}/processed")
        vehicles_metadata = get_appropriate_timetable(datetime, vehicles_base_path)

        if not schedule_metadata["date"] == vehicles_metadata["date"]:
            ctx.logger(f"Schedule date does not match tracked vehicle data for line {line}")
            ctx.logger(f"Schedule date: {schedule_metadata['date']}")
            ctx.logger(f"Tracking data date: {vehicles_metadata['date']}")
            continue

        try:
            vehicles = pd.read_csv(vehicles_metadata["path"], index_col=0, parse_dates=["datetime"])
        except:
            ctx.logger(f"Couldn't get vehicle data for line {line} at path: {vehicles_metadata['path']}")
            continue
        try:
            schedule = pd.read_csv(schedule_metadata["path"], index_col=0, parse_dates=["datetime"])
        except:
            ctx.logger(f"Couldn't get schedule data for line {line} at path: {schedule_metadata['path']}")
            continue

        all_estimates = list()
        for direction in range(2):
            vehicles_direction = vehicles[vehicles["direction_id"] == direction]
            schedule_direction = schedule[schedule["direction_id"] == direction]
            stations = pd.read_csv(
                f"data/line_info/{line}/{line}_{direction}_stations.csv", index_col=0
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
            all_estimates, schedule, schedule_metadata["date"], datetime.to_iso8601_string()
        )

    # write master summary
    formatted_time = schedule_metadata["date"]  # Takes the date of the last processed schedule
    ctx.datastore.write_json(f"summaries/{agency}/{formatted_time}.json", master_summary)
    
    return 0
