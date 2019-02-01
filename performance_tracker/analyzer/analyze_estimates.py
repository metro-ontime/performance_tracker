import pandas as pd


def match_times(stop_id, estimates, schedule):
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


def match_arrivals_with_schedule(estimated_trips, schedule_direction):
    matched_estimates = pd.concat(
        [
            match_times(
                stop_id,
                stop_estimates,
                schedule_direction[schedule_direction["stop_id"] == stop_id],
            )
            for stop_id, stop_estimates in estimated_trips.groupby(["stop_id"])
        ]
    )
    matched_estimates["since_scheduled"] = (
        matched_estimates["datetime"] - matched_estimates["closest_scheduled"]
    )
    return matched_estimates


def get_previous_stop_times(stop_id, stop_estimates):
    stop_estimates = stop_estimates.set_index(
        pd.DatetimeIndex(stop_estimates["datetime"])
    ).sort_index()
    stop_estimates["prev_stop_time"] = stop_estimates["datetime"].shift()
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
