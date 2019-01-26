import pandas as pd
import pendulum

# get processed vehicle, estimate arrival times

agency = "lametro-rail"
now = pendulum.now("America/Los_Angeles")
today = now.format("YYYY-MM-DD")


def estimate_arrivals(trip_id, trip, stations):
    trip["estimate"] = False
    stations["estimate"] = True
    trip_est = stations
    trip_est["trip_id"] = trip_id
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
    select["datetime_round"] = pd.DatetimeIndex(select.datetime).round("S")
    select["stop_id"] = pd.to_numeric(select.stop_id, downcast="integer")
    select = select.dropna(subset=["datetime"])
    return select


def match_arrivals_with_schedule(stop_id, arrivals, schedule):
    estimates = arrivals.set_index(pd.DatetimeIndex(est["datetime"])).sort_index()
    estimates.loc[:, "closest_scheduled"] = estimates.datetime.apply(
        # TO DO: & where schedule matches stop_id
        lambda x: schedule.index[schedule.index.get_loc(x, method="nearest")]
    )
    estimates["closest_scheduled"] = pd.DatetimeIndex(estimates["closest_scheduled"])
    return estimates


for line in range(801, 807):
    # load vehicles
    vehicle_positions = pd.read_csv(
        f"data/vehicle_tracking/processed/{line}_{lametro-rail}/{today}.csv",
        index_col=0,
        parse_dates=["datetime"],
    )
    # load schedule
    schedule = pd.read_csv(f"data/schedule/{line}_{agency}/{today}.csv", index_col=0)

    all_est = []
    for direction in range(2):
        vehicles_direction = vehicle_positions[
            vehicle_positions["direction"] == direction
        ]
        schedule_direction = schedule[schedule["direction"] == direction]
        stations_direction = pd.read_csv(
            f"data/line_info/{line}/{line}_{direction}_stations.csv", index_col=0
        )
        trips_direction = vehicles_direction[
            ["datetime_local_iso8601", "trip_id", "relative_position", "estimate"]
        ].groupby(["trip_id"])

        estimated_trips = [
            estimate_arrivals(trip_id, trip, stations_direction)
            for trip_id, trip in trips
        ]

        all_est[direction] = pd.concat(estimated_trips)
        # remove estimates that are NaT

        # for each estimated arrival, find closest scheduled stop & get time diff
        all_est[direction] = pd.concat(
            [
                match_arrivals_with_schedule(stop_id, stop_estimates, schedule)
                for stop_id, stop_estimates in all_est.groupby(["stop_id"])
            ]
        )
        all_est[direction]["difference"] = (
            all_est[direction]["datetime"] - all_est[direction]["closest_scheduled"]
        )
    # concat estimates into 1 df
    all_estimates = pd.concat(all_est)
    # write to
    estimated_arrivals_path = f"data/estimates/{line}_{agency}/{today}.csv"
