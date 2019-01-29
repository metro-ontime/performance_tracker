import pandas as pd


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
