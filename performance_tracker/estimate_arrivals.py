import pandas as pd
import pendulum
import os
import json
from analyzer.estimate_arrivals import estimate_arrivals_by_trip
from analyzer.analyze_estimates import (
    match_arrivals_with_schedule,
    match_previous_stop_times,
)
from helpers.timing import get_appropriate_schedule, get_appropriate_vehicle_positions
from analyzer.summary import statistic_summary

agency = "lametro-rail"
datetime = pendulum.now("America/Los_Angeles")


for line in range(801, 807):
    schedule = get_appropriate_schedule(datetime, f"data/schedule/{line}_{agency}")
    vehicle_positions = get_appropriate_vehicle_positions(
        datetime, f"data/vehicle_tracking/processed/{line}_{agency}"
    )
    if not schedule["date"] == vehicle_positions["date"]:
        continue
    vehicle_positions = pd.read_csv(
        vehicle_positions["path"], index_col=0, parse_dates=["datetime"]
    )
    schedule = schedule["data"]

    all_estimates = list()
    for direction in range(2):
        vehicles_direction = vehicle_positions[
            vehicle_positions["direction_id"] == direction
        ]
        schedule_direction = schedule[schedule["direction_id"] == direction]
        stations = pd.read_csv(
            f"data/line_info/{line}/{line}_{direction}_stations.csv", index_col=0
        )
        trips = vehicles_direction.groupby(["trip_id"])

        ### Heavy calculations
        estimates = estimate_arrivals_by_trip(trips, stations, direction)
        estimates = match_arrivals_with_schedule(estimates, schedule_direction)
        estimates = match_previous_stop_times(estimates)
        ###

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

    summary = statistic_summary(all_estimates, schedule, datetime.to_iso8601_string())
    # write summary
    summary_dir = f"data/summaries/{line}_{agency}"
    os.makedirs(summary_dir, exist_ok=True)
    formatted_time = datetime.format("YYYY-MM-DD")
    summary_path = os.path.join(summary_dir, formatted_time) + ".json"
    with open(summary_path, "w") as outfile:
        json.dump(summary, outfile)
