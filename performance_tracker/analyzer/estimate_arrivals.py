import pandas as pd


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
