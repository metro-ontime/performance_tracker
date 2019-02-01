import pandas as pd


def statistic_summary(estimates, schedule, timestamp):
    since_scheduled = estimates.since_scheduled
    since_prev_stop = estimates.since_prev_stop

    summary = {}
    summary["timestamp"] = timestamp
    summary["total_arrivals_analyzed"] = len(estimates)
    summary["total_scheduled_arrivals"] = len(schedule)
    summary["coverage"] = len(estimates) / len(schedule)
    summary["ontime"] = {}

    summary["mean_secs"] = since_scheduled.mean().total_seconds()
    summary["std_secs"] = since_scheduled.std().total_seconds()
    summary["mean_time_between"] = since_prev_stop.mean().total_seconds()

    # Get 1 minute window stats
    late_window = pd.to_timedelta("1 minute")
    early_window = pd.to_timedelta("-1 days 23:59:00")
    summary["ontime"]["1_min"] = len(
        since_scheduled[
            (since_scheduled < late_window) & (since_scheduled > early_window)
        ]
    )

    # Get 2 minute window stats
    late_window = pd.to_timedelta("2 minutes")
    early_window = pd.to_timedelta("-1 days 23:58:00")
    summary["ontime"]["2_min"] = len(
        since_scheduled[
            (since_scheduled < late_window) & (since_scheduled > early_window)
        ]
    )

    # Get 3 minute window stats
    late_window = pd.to_timedelta("3 minutes")
    early_window = pd.to_timedelta("-1 days 23:57:00")
    summary["ontime"]["3_min"] = len(
        since_scheduled[
            (since_scheduled < late_window) & (since_scheduled > early_window)
        ]
    )

    # Get 4 minute window stats
    late_window = pd.to_timedelta("4 minutes")
    early_window = pd.to_timedelta("-1 days 23:56:00")
    summary["ontime"]["4_min"] = len(
        since_scheduled[
            (since_scheduled < late_window) & (since_scheduled > early_window)
        ]
    )

    # Get 5 minute window stats
    late_window = pd.to_timedelta("5 minutes")
    early_window = pd.to_timedelta("-1 days 23:55:00")
    summary["ontime"]["5_min"] = len(
        since_scheduled[
            (since_scheduled < late_window) & (since_scheduled > early_window)
        ]
    )

    return summary
