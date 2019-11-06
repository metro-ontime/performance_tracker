import pandas as pd
import pendulum
import os
import json
from library.analyzer.estimate_arrivals import estimate_arrivals_by_trip
from library.analyzer.analyze_estimates import (
    match_arrivals_with_schedule,
    match_previous_stop_times,
)

def estimate_arrivals(ctx ,datetime):
    from library.helpers.timing import get_appropriate_timetable
    from library.analyzer.summary import statistic_summary

    agency = "lametro-rail"

    master_summary = {}

    for line in range(801, 807):
        schedule_base_path = f"data/tmp/schedule/{agency}/{line}"
        schedule_meta = get_appropriate_timetable(datetime, schedule_base_path)
        print(schedule_meta["path"])
        vehicles_base_path = f"data/tmp/tracking/{agency}/{line}/processed"
        vehicles_meta = get_appropriate_timetable(datetime, vehicles_base_path)
        print(vehicles_meta["path"])

        if not schedule_meta["date"] == vehicles_meta["date"]:
            continue

        vehicles = pd.read_csv(vehicles_meta["path"], index_col=0, parse_dates=["datetime"])
        schedule = pd.read_csv(schedule_meta["path"], index_col=0, parse_dates=["datetime"])

        all_estimates = list()
        for direction in range(2):
            vehicles_direction = vehicles[vehicles["direction_id"] == direction]
            schedule_direction = schedule[schedule["direction_id"] == direction]
            stations = pd.read_csv(
                f"data/line_info/{line}/{line}_{direction}_stations.csv", index_col=0
            )
            trips = vehicles_direction.groupby(["trip_id"])

            print(
                f"Beginning heavy calculations for line {line} and direction {direction} at",
                pendulum.now("UTC"),
            )
            ### Heavy calculations
            estimates = estimate_arrivals_by_trip(trips, stations, direction)
            print("Estimate arrivals by trip: completed at ", pendulum.now("UTC"))
            estimates = match_arrivals_with_schedule(estimates, schedule_direction)
            print("Match arrivals with schedule: completed at ", pendulum.now("UTC"))
            estimates = match_previous_stop_times(estimates)
            print("Match previous stop times: completed at ", pendulum.now("UTC"))
            ###
            print(f"Completed heavy calculations for line {line} and direction {direction} at", pendulum.now("UTC"))

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
            all_estimates, schedule, schedule_meta["date"], datetime.to_iso8601_string()
        )

    # write master summary
    summary_dir = f"data/summaries/{agency}"
    os.makedirs(summary_dir, exist_ok=True)
    formatted_time = schedule_meta["date"]  # Takes the date of the last processed schedule
    summary_path = os.path.join(summary_dir, formatted_time) + ".json"
    with open(summary_path, "w") as outfile:
        json.dump(master_summary, outfile)
    
    return 0
