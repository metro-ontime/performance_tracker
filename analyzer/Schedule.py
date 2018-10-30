import pandas as pd
from datetime import timedelta
from App.classes.Stations import splitStopIds

class Schedule:
    def __init__(self, date, line_id, full_schedule):
        self.date = date
        self.times = makeSchedule(full_schedule, line_id, date)

def makeSchedule(full_schedule, line_id, date):
    full_schedule = splitStopIds(full_schedule, 'stop_id') #don't do this here, unnecessary repetition
    line_schedule = full_schedule.groupby('line_id').get_group(line_id)
    line_schedule = scheduleTimeToDateTime(line_schedule, date)
    return line_schedule

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
