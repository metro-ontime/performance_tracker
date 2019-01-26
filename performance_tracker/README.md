# App Structure

This app is a set of scripts that need to be run at various frequencies. The schedule below defines the function and frequency of each script.

## Schedule:

Get current vehicle positions and save to raw json documents:
    script: query_vehicles.sh
    freq: every minute

Get current predictions and save to raw json documents (disabled by default for disk space)z:
    script: query_predictions.sh
    freq: every minute

Get current schedule, process and (optionally) upload to S3:
    script: query_schedule.sh (or upload_schedule.sh)
    freq: once per day at 2 or 3am

Process vehicles (get relative_position, datetime, trip_id and direction), produce estimated arrival times for each trip, optionally upload:
    script: process_vehicles.sh (or process_upload_vehicles.sh)
    freq: every 30 mins
    
Use schedule to prepare list of unique stops (use with caution, schedule doesn't always include all stops):
    script: prepare_stop_list.sh
    freq: Once only required (unless new stops are added in future)