import pandas as pd
from datetime import timedelta
from .stations import split_stop_ids

class Schedule:
    def __init__(self, date, line_id, full_schedule, trips):
        self.date = date
        self.times = makeSchedule(full_schedule, line_id, date, trips)

def makeSchedule(schedule, line_id, date, trips):
    schedule = filter_by_trips(schedule, trips)
    schedule = split_stop_ids(schedule, 'stop_id') #don't do this here, unnecessary repetition
    schedule = schedule.groupby('line_id').get_group(line_id)
    schedule = scheduleTimeToDateTime(schedule, date)
    return schedule

def filter_by_trips(schedule, trips):
    schedule.loc[:, 'today'] = schedule.trip_id.apply(lambda trip: trip in trips)
    return schedule[schedule.today == True]

def scheduleTimeToDateTime(schedule, date):
    schedule['arrival_hour'] = schedule.arrival_time.apply(lambda row: int(str(row)[0:2]))
    schedule['arrival_min'] = schedule.arrival_time.apply(lambda row: int(str(row)[3:5]))

    today = schedule[schedule['arrival_hour'] < 24]
    tomorrow = schedule[schedule['arrival_hour'] >= 24]

    today['datetime'] = today.apply(lambda row: makeDateTime(date, row['arrival_time']), axis=1)
    tomorrow['datetime'] = tomorrow.apply(lambda row: makeTomorrowDateTime(date, row['arrival_hour'], row['arrival_min']), axis=1)
    
    schedule = pd.concat([today, tomorrow])
    return schedule

def hourMinusDay(hour):
    new_hour = int(hour) - 24
    return "{0:0=2d}".format(new_hour)

def makeDateTime(date, time):
    return pd.to_datetime(date + ' ' + time)

def makeTomorrowDateTime(date, hour, minute):
    return pd.to_datetime(date + ' ' + hourMinusDay(hour) + ':' + str(minute) + ':00') + timedelta(days=1)
