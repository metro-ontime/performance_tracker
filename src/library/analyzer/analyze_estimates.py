import pandas as pd


def match_times(stop_id, estimates, schedule):
    # This technique finds the closest scheduled time to actual arrivals
    # This is flawed since it does not account for scheduled arrivals where
    # a train never arrived.
    # It's difficult to search the other way around however, since our estimated
    # arrival times are incomplete (see "select.dropna" in "estimate_arrivals").
    # If we search for the closest estimated arrival to each scheduled stop,
    # we will get some that are far apart because the actual train was likely associated
    # with a different scheduled stop time.
    # This way seems to be fairer on Metro, but we are open to improvements!

    # Try clause is here because there was an unexplained bug occurring on April 10 2019 with data inputs from around 1:35pm. There was an index (-1) out of range error.
    # Exact cause of the issue is still uncertain but there was a vehicle position observation out of range on the blue line at that time.
    try:
        estimates.loc[:, "closest_scheduled"] = estimates.datetime_utc.apply(
            lambda x: schedule.index[schedule.index.get_loc(x, method="nearest")]
        )
        estimates.loc[:, "closest_scheduled"] = pd.DatetimeIndex(
            estimates["closest_scheduled"]
        )
        return estimates
    except:
        return None


def match_arrivals_with_schedule(estimated_trips, schedule_direction):
    schedule_direction.loc[:,"datetime_utc"] = pd.to_datetime(schedule_direction["datetime"], utc=True)
    estimated_trips.loc[:,"datetime_utc"] = pd.to_datetime(estimated_trips["datetime"], utc=True)
    schedule_direction = schedule_direction.set_index(pd.DatetimeIndex(schedule_direction["datetime_utc"])).sort_index()
    matched_estimates = [
        match_times(
            stop_id,
            stop_estimates,
            schedule_direction[schedule_direction["stop_id"] == stop_id],
        )
        for stop_id, stop_estimates in estimated_trips.groupby(["stop_id"])
    ]
    matched_estimates = [x for x in matched_estimates if x is not None]
    matched_estimates = pd.concat(matched_estimates)
    matched_estimates["since_scheduled"] = (
        matched_estimates["datetime_utc"] - matched_estimates["closest_scheduled"]
    )
    return matched_estimates


def get_previous_stop_times(stop_id, stop_estimates):
    stop_estimates = stop_estimates.set_index(
        pd.DatetimeIndex(stop_estimates["datetime"])
    ).sort_index()
    stop_estimates.loc[:, "prev_stop_time"] = stop_estimates["datetime"].shift()
    return stop_estimates


def match_previous_stop_times(estimates):
    matched_estimates = pd.concat(
        [
            get_previous_stop_times(stop_id, stop_estimates)
            for stop_id, stop_estimates in estimates.groupby(["stop_id"])
        ]
    )
    matched_estimates["since_prev_stop"] = (
        matched_estimates["datetime"] - matched_estimates["prev_stop_time"]
    )
    return matched_estimates
