import pendulum
import sys

sys.path.append("../performance_tracker")

from helpers.timing import (
    get_latest_schedule,
    get_appropriate_schedule,
    first_scheduled_arrival,
    last_scheduled_arrival,
)


line = 804
agency = "lametro-rail"


def test_arbitrary_schedule():
    sample_date = pendulum.datetime(2019, 1, 31, 12, tz="America/Los_Angeles")
    latest_schedule_path = "../sample_data/schedule/804_lametro-rail/2019-01-31.csv"

    assert (
        get_appropriate_schedule(line, agency, sample_date, "../sample_data/schedule")
        == latest_schedule_path
    )

    assert first_scheduled_arrival(latest_schedule_path) == pendulum.parse(
        "2019-01-31T03:45:00-08:00"
    )

    assert last_scheduled_arrival(latest_schedule_path) == pendulum.parse(
        "2019-02-01T02:06:00-08:00"
    )


def test_after_midnight():
    sample_date = pendulum.datetime(2019, 1, 29, 1, tz="America/Los_Angeles")
    latest_schedule_path = "../sample_data/schedule/804_lametro-rail/2019-01-28.csv"

    assert (
        get_appropriate_schedule(line, agency, sample_date, "../sample_data/schedule")
        == latest_schedule_path
    )
