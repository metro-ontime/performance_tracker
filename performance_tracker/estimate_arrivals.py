import pandas as pd
import pendulum
import os
import json
from analyzer.estimate_arrivals import estimate_arrivals
from analyzer.match_estimates import match_arrivals_with_schedule
from analyzer.stats import statistic_summary

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
        stations_direction = pd.read_csv(
            f"data/line_info/{line}/{line}_{direction}_stations.csv", index_col=0
        )
        trips_direction = vehicles_direction.groupby(["trip_id"])

        estimated_trips = [
            estimate_arrivals(trip_id, trip, stations_direction, direction)
            for trip_id, trip in trips_direction
        ]

        estimated_trips = pd.concat(estimated_trips)

        # for each estimated arrival, find closest scheduled stop & get time diff
        matched_estimates = pd.concat(
            [
                match_arrivals_with_schedule(
                    stop_id,
                    stop_estimates,
                    schedule_direction[schedule_direction["stop_id"] == stop_id],
                )
                for stop_id, stop_estimates in estimated_trips.groupby(["stop_id"])
            ]
        )
        matched_estimates["difference"] = (
            matched_estimates["datetime"] - matched_estimates["closest_scheduled"]
        )
        all_estimates.append(matched_estimates)
    # concat estimates into 1 df
    all_estimates = pd.concat(all_estimates)[
        ["datetime", "stop_id", "direction_id", "closest_scheduled", "difference"]
    ]

    summary = statistic_summary(all_estimates, schedule)
    # write summary
    summary_dir = f"data/summaries/{line}_{agency}"
    os.makedirs(summary_dir, exist_ok=True)
    summary_path = os.path.join(summary_dir, today) + ".json"
    with open(summary_path, "w") as outfile:
        json.dump(summary, outfile)

    # currently not writing estimated arrivals
    # estimated_arrivals_path = f"data/estimates/{line}_{agency}"
    # os.makedirs(estimated_arrivals_path, exist_ok=True)
    # all_estimates.to_csv(os.path.join(estimated_arrivals_path, today) + ".csv")
