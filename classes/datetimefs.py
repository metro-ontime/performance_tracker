import re
import glob
import pendulum

# This class assumes we are using a file naming system
# that looks like:
# /path/to/fs/YYYY-MM-DD/HH:mm:ss
# e.g. ~/myrepo/data/2018-12-20/22:57:05


class DateTimeFS:
    def __init__(self, path_to_fs):
        self.root = path_to_fs + "/"

    def get_all_dates(self):
        date_paths = glob.glob(self.root + "*")
        return sorted([extract_date(self.root, path) for path in date_paths])

    def get_datetimes_by_date(self, datetime):
        path_base = self.root + datetime.format("YYYY-MM-DD") + "/"
        time_paths = glob.glob(path_base + "*")
        return sorted([extract_datetime(self.root, path) for path in time_paths])

    def get_datetimes_in_range(self, start, end):
        all_dates = self.get_all_dates()
        start_date = pendulum.from_format(start.format("YYYY-MM-DD"), "YYYY-MM-DD")
        end_date = pendulum.from_format(end.format("YYYY-MM-DD"), "YYYY-MM-DD")
        select_dates = list(
            filter(lambda date: date >= start_date and date <= end_date, all_dates)
        )
        for date in select_dates:
            files = glob.glob(self.root + date.format("YYYY-MM-DD") + "/*")
            datetimes = self.get_datetimes_by_date(date)
            select_datetimes = list(
                filter(
                    lambda datetime: datetime >= start and datetime <= end, datetimes
                )
            )
        return select_datetimes

    def get_files_in_range(self, extension, start, end):
        valid_datetimes = self.get_datetimes_in_range(start, end)
        return [
            construct_filename(self.root, datetime, extension)
            for datetime in valid_datetimes
        ]


def construct_filename(path_base, datetime, extension):
    return (
        path_base
        + datetime.format("YYYY-MM-DD")
        + "/"
        + datetime.format("HH:mm:ss")
        + extension
    )


def extract_datetime(path_to_dt, full_path):
    string_to_match = f"(?:{path_to_dt})([0-9]+-[0-9]+-[0-9]+)/([0-9]+:[0-9]+:[0-9]+)"
    dateinfo = re.match(string_to_match, full_path).groups()
    return pendulum.from_format(dateinfo[0] + "T" + dateinfo[1], "YYYY-MM-DDTHH:mm:ss")


def extract_date(path_to_dt, full_path):
    string_to_match = f"(?:{path_to_dt})([0-9]+-[0-9]+-[0-9]+)"
    dateinfo = re.match(string_to_match, full_path).groups()
    return pendulum.from_format(dateinfo[0], "YYYY-MM-DD")


def extract_time(path_to_dt, full_path):
    string_to_match = f"(?:{path_to_dt})([0-9]+:[0-9]+:[0-9]+)"
    dateinfo = re.match(string_to_match, full_path).groups()
    return pendulum.from_format(dateinfo[0], "HH:mm:ss")
