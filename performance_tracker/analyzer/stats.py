import pandas as pd


def statistic_summary(estimates, schedule):
    series = estimates.difference

    summary = {}
    summary["total_arrivals_analyzed"] = len(estimates)
    summary["total_scheduled_arrivals"] = len(schedule)
    summary["coverage"] = len(estimates) / len(schedule)
    summary["ontime"] = {}

    summary["mean_secs"] = series.mean().total_seconds()
    summary["std_secs"] = series.std().total_seconds()

    # Get 1 minute window stats
    late_window = pd.to_timedelta("1 minute")
    early_window = pd.to_timedelta("-1 days 23:59:00")
    summary["ontime"]["1_min"] = len(
        series[(series < late_window) & (series > early_window)]
    )

    # Get 2 minute window stats
    late_window = pd.to_timedelta("2 minutes")
    early_window = pd.to_timedelta("-1 days 23:58:00")
    summary["ontime"]["2_min"] = len(
        series[(series < late_window) & (series > early_window)]
    )

    # Get 3 minute window stats
    late_window = pd.to_timedelta("3 minutes")
    early_window = pd.to_timedelta("-1 days 23:57:00")
    summary["ontime"]["3_min"] = len(
        series[(series < late_window) & (series > early_window)]
    )

    # Get 4 minute window stats
    late_window = pd.to_timedelta("4 minutes")
    early_window = pd.to_timedelta("-1 days 23:56:00")
    summary["ontime"]["4_min"] = len(
        series[(series < late_window) & (series > early_window)]
    )

    # Get 5 minute window stats
    late_window = pd.to_timedelta("5 minutes")
    early_window = pd.to_timedelta("-1 days 23:55:00")
    summary["ontime"]["5_min"] = len(
        series[(series < late_window) & (series > early_window)]
    )

    return summary
