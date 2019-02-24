import os
import re
import glob
import pendulum

# This class assumes we are using a file naming system
# that looks like:
# /path/to/fs/YYYY-MM-DD/HH:mm:ss
# e.g. ~/myrepo/data/2018-12-20/22:57:05


class DateTimeFS:
    def __init__(self, path_to_fs):
        self.root = path_to_fs

    def get_all_dates(self, tz="UTC"):
        path_to_search = os.path.join(self.root, "*")
        date_paths = glob.glob(path_to_search)
        return sorted([extract_date(self.root, path, tz=tz) for path in date_paths])

    def get_datetimes_by_date(self, datetime, tz="UTC"):
        path_base = os.path.join(self.root, datetime.format("YYYY-MM-DD"))
        time_paths = glob.glob(os.path.join(path_base, "*"))
        return sorted([extract_datetime(self.root, path, tz=tz) for path in time_paths])

    def get_datetimes_in_range(self, start, end):
        # filter by DATES YYYY-MM-DD first to save time
        all_dates = self.get_all_dates()
        start_date = start.start_of("day")
        end_date = end.end_of("day")
        select_dates = list(
            filter(lambda date: date >= start_date and date <= end_date, all_dates)
        )
        # Then filter by time within dates
        select_datetimes = list()
        for date in select_dates:
            files = glob.glob(os.path.join(self.root, date.format("YYYY-MM-DD"), "*"))
            datetimes = self.get_datetimes_by_date(date)
            select_datetimes.extend(
                list(
                    filter(
                        lambda datetime: datetime >= start and datetime <= end,
                        datetimes,
                    )
                )
            )
        return select_datetimes

    def get_filenames_in_range(self, extension, start, end):
        valid_datetimes = self.get_datetimes_in_range(start, end)
        return [
            construct_filename(self.root, datetime, extension)
            for datetime in valid_datetimes
        ]


def construct_filename(path_base, datetime, extension):
    return (
        os.path.join(
            path_base, datetime.format("YYYY-MM-DD"), datetime.format("HH:mm:ss")
        )
        + extension
    )


def extract_datetime(path_to_dt, full_path, tz="UTC"):
    string_to_match = f"(?:{path_to_dt}/)([0-9]+-[0-9]+-[0-9]+)/([0-9]+:[0-9]+:[0-9]+)"
    dateinfo = re.match(string_to_match, full_path).groups()
    return pendulum.from_format(
        dateinfo[0] + "T" + dateinfo[1], "YYYY-MM-DDTHH:mm:ss", tz=tz
    )


def extract_date(path_to_dt, full_path, tz="UTC"):
    string_to_match = f"(?:{path_to_dt}/)([0-9]+-[0-9]+-[0-9]+)"
    dateinfo = re.match(string_to_match, full_path).groups()
    return pendulum.from_format(dateinfo[0], "YYYY-MM-DD", tz=tz)


def extract_time(path_to_dt, full_path, tz="UTC"):
    string_to_match = f"(?:{path_to_dt}/)([0-9]+:[0-9]+:[0-9]+)"
    dateinfo = re.match(string_to_match, full_path).groups()
    return pendulum.from_format(dateinfo[0], "HH:mm:ss", tz=tz)
