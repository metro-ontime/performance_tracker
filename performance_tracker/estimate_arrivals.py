import pandas as pd
import pendulum
import os
import json
from analyzer.estimate_arrivals import estimate_arrivals_by_trip
from analyzer.analyze_estimates import (
    match_arrivals_with_schedule,
    match_previous_stop_times,
)
from analyzer.summary import statistic_summary

agency = "lametro-rail"
now = pendulum.now("America/Los_Angeles")
today = now.format("YYYY-MM-DD")
yesterday = pendulum.yesterday("America/Los_Angeles").format("YYYY-MM-DD")


for line in range(801, 807):
    vehicle_positions_path = (
        f"data/vehicle_tracking/processed/{line}_{agency}/{today}.csv"
    )
    if not os.path.exists(vehicle_positions_path):
        vehicle_positions_path = (
            f"data/vehicle_tracking/processed/{line}_{agency}/{yesterday}.csv"
        )

    schedule_path = f"data/schedule/{line}_{agency}/{today}.csv"
    if not os.path.exists(schedule_path):
        schedule_path = f"data/schedule/{line}_{agency}/{yesterday}.csv"

    vehicle_positions = pd.read_csv(
        vehicle_positions_path, index_col=0, parse_dates=["datetime"]
    )
    schedule = pd.read_csv(schedule_path, index_col=0)

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

    summary = statistic_summary(all_estimates, schedule, now.to_iso8601_string())
    # write summary
    summary_dir = f"data/summaries/{line}_{agency}"
    os.makedirs(summary_dir, exist_ok=True)
    summary_path = os.path.join(summary_dir, today) + ".json"
    with open(summary_path, "w") as outfile:
        json.dump(summary, outfile)
