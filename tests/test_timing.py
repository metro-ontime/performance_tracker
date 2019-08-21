import pendulum
import pytest
import sys

sys.path.append("src")

from library.helpers.timing import (
    get_appropriate_timetable,
    get_date_if_exists_otherwise_previous,
    check_datetime,
)


line = 804
agency = "lametro-rail"


@pytest.mark.skip
def test_arbitrary_schedule():
    sample_date = pendulum.datetime(2019, 1, 31, 12, tz="America/Los_Angeles")
    schedule_path = "../sample_data/schedule/804_lametro-rail/2019-01-31.csv"

    assert (
        get_appropriate_timetable(
            sample_date, f"../sample_data/schedule/{line}_{agency}"
        )["path"]
        == schedule_path
    )

    assert (
        get_date_if_exists_otherwise_previous(
            sample_date, f"../sample_data/schedule/{line}_{agency}"
        )
        == sample_date
    )


@pytest.mark.skip
def test_after_midnight():
    sample_date = pendulum.datetime(2019, 1, 29, 1, tz="America/Los_Angeles")
    schedule_path = "../sample_data/schedule/804_lametro-rail/2019-01-28.csv"

    assert (
        get_appropriate_timetable(
            sample_date, f"../sample_data/schedule/{line}_{agency}"
        )["path"]
        == schedule_path
    )


@pytest.mark.skip
def test_before_schedule_download():
    sample_date = pendulum.datetime(2019, 2, 1, 1, tz="America/Los_Angeles")
    assert get_date_if_exists_otherwise_previous(
        sample_date, f"../sample_data/schedule/{line}_{agency}"
    ) == sample_date.subtract(days=1)


def test_checks():
    sample_date = pendulum.datetime(2019, 2, 1, 1, tz="America/Los_Angeles")
    dates = ["2019-01-31"]
    assert check_datetime(sample_date, dates, "YYYY-MM-DD") == False
    sample_date = pendulum.datetime(2019, 2, 1, 1, tz="America/Los_Angeles")
    dates = ["2019-01-31", "2019-02-01"]
    assert check_datetime(sample_date, dates, "YYYY-MM-DD") == True


def test_empty_dates():
    sample_date = pendulum.datetime(2019, 2, 1, 1, tz="America/Los_Angeles")
    with pytest.raises(Exception):
        check_datetime(sample_date, [], "YYYY-MM-DD")
