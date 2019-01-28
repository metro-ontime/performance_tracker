import pandas as pd
import pendulum
import os

# get processed vehicle, estimate arrival times

agency = "lametro-rail"
now = pendulum.now("America/Los_Angeles")
today = now.format("YYYY-MM-DD")


def estimate_arrivals(trip_id, trip, stations, direction):
    trip["estimate"] = False
    stations["estimate"] = True
    trip_est = stations
    trip_est["trip_id"] = trip_id
    trip_est["direction_id"] = direction
    combined = trip.append(trip_est)
    combined = combined.sort_values("relative_position")
    combined = combined.reset_index(drop=True)
    combined[
        "previous_pos"
    ] = (
        combined.relative_position.shift()
    )  # shift vals to move adjacent position and date data into each row
    combined["next_pos"] = combined.relative_position.shift(-1)
    combined["previous_dt"] = combined.datetime.shift()
    combined["next_dt"] = combined.datetime.shift(-1)
    select = combined[combined["estimate"] == True]
    select["weight"] = (select.relative_position - select.previous_pos) / (
        select.next_pos - select.previous_pos
    )
    select["time_interpolation"] = (select.next_dt - select.previous_dt) * select.weight
    select["datetime"] = select.previous_dt + select.time_interpolation
    select["datetime"] = pd.DatetimeIndex(select.datetime).round("S")
    select["stop_id"] = pd.to_numeric(select.stop_id, downcast="integer")
    # Some station estimates cannot be reliably estimated using this
    # technique and will have datetime = NaT, so we remove them.
    select = select.dropna(subset=["datetime"])
    return select


def match_arrivals_with_schedule(stop_id, estimates, schedule):
    schedule = schedule.set_index(pd.DatetimeIndex(schedule["datetime"])).sort_index()
    # This technique finds the closest scheduled time to actual arrivals
    # This is flawed since it does not account for scheduled arrivals where
    # a train never arrived.
    # It's difficult to search the other way around however, since our estimated
    # arrival times are incomplete (see "select.dropna" in "estimate_arrivals").
    # If we search for the closest estimated arrival to each scheduled stop,
    # we will get some that are far apart because the actual train was likely associated
    # with a different scheduled stop time.
    # This way seems to be fairer on Metro, but we are open to improvements!
    estimates.loc[:, "closest_scheduled"] = estimates.datetime.apply(
        lambda x: schedule.index[schedule.index.get_loc(x, method="nearest")]
    )
    estimates["closest_scheduled"] = pd.DatetimeIndex(estimates["closest_scheduled"])
    return estimates


for line in range(801, 807):
    vehicle_positions = pd.read_csv(
        f"data/vehicle_tracking/processed/{line}_{agency}/{today}.csv",
        index_col=0,
        parse_dates=["datetime"],
    )
    schedule = pd.read_csv(f"data/schedule/{line}_{agency}/{today}.csv", index_col=0)

    all_est = list()
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

        all_est.append(pd.concat(estimated_trips))

        # for each estimated arrival, find closest scheduled stop & get time diff
        all_est[direction] = pd.concat(
            [
                match_arrivals_with_schedule(
                    stop_id,
                    stop_estimates,
                    schedule_direction[schedule_direction["stop_id"] == stop_id],
                )
                for stop_id, stop_estimates in all_est[direction].groupby(["stop_id"])
            ]
        )
        all_est[direction]["difference"] = (
            all_est[direction]["datetime"] - all_est[direction]["closest_scheduled"]
        )
    # concat estimates into 1 df
    all_estimates = pd.concat(all_est)[
        ["datetime", "stop_id", "direction_id", "closest_scheduled", "difference"]
    ]
    # write to
    estimated_arrivals_path = f"data/estimates/{line}_{agency}"
    os.makedirs(estimated_arrivals_path, exist_ok=True)
    all_estimates.to_csv(os.path.join(estimated_arrivals_path, today) + ".csv")
