import os
import pendulum
from analyzer.gtfs import load_and_parse_schedule

start_datetime = pendulum.today("UTC")
end_datetime = start_datetime.add(hours=27)
line_no = 804

datestring = start_datetime.format("YYYY-MM-DD")
os.makedirs(f"data/schedule/{line_no}", exist_ok=True)

schedule = load_and_parse_schedule(line_no, start_datetime, end_datetime)
schedule.to_csv(f"data/schedule/{line_no}/{datestring}.csv")
