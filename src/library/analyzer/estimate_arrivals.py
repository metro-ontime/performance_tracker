import pandas as pd


def estimate_arrivals(trip_id, trip, stations, direction):
    trip.loc[:, "estimate"] = False
    stations.loc[:, "estimate"] = True
    trip_est = stations
    trip_est.loc[:, "trip_id"] = trip_id
    trip_est.loc[:, "direction_id"] = direction 
    combined = trip.append(trip_est)
    combined = combined.sort_values("relative_position")
    combined = combined.reset_index(drop=True)
    # shift vals to move adjacent position and date data into each row
    combined.loc[:, "previous_pos"] = combined.relative_position.shift()
    combined.loc[:, "next_pos"] = combined.relative_position.shift(-1)
    combined.loc[:, "previous_dt"] = combined.datetime.shift()
    combined.loc[:, "next_dt"] = combined.datetime.shift(-1)
    select = combined[combined["estimate"] == True]
    select.loc[:, "weight"] = (select.relative_position - select.previous_pos) / (
        select.next_pos - select.previous_pos
    )
    select.loc[:, "time_interpolation"] = (
        select.next_dt - select.previous_dt
    ) * select.weight
    select.loc[:, "datetime"] = select.previous_dt + select.time_interpolation
    select.loc[:, "datetime"] = pd.DatetimeIndex(select.datetime).round("S")
    select.loc[:, "stop_id"] = pd.to_numeric(select.stop_id, downcast="integer")
    # Some station estimates cannot be reliably estimated using this
    # technique and will have datetime = NaT, so we remove them.
    select = select.dropna(subset=["datetime"])
    return select


def estimate_arrivals_by_trip(trips, stations, direction):
    return pd.concat(
        [
            estimate_arrivals(trip_id, trip, stations, direction)
            for trip_id, trip in trips
        ]
    )
