from pandas import read_csv
from .tracker import selectAnalysisWindow


def load_and_parse_schedule(line_no, start_datestring, end_datestring):

    return selectAnalysisWindow(line.getScheduleWithCoordinates(), start_date, end_date)
