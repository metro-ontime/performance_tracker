# Metro Performance Monitor

### A Health App for the Los Angeles Metro Rail System

This project, incubated at Hack for LA, tracks LA Metro trains and provides up to date statistics summarizing daily, weekly, monthly and annual performance. Our mission is to monitor and report the number of both on-time and late train arrivals on an ongoing basis for all Metro rail lines in Los Angeles. By publishing these statistics and open-sourcing our methodology, we aim to give riders an accurate and unvarnished picture of the system's state over time. Hopefully, this will correct any public misperception of Metro's track record and help inform decision-makers when assessing future improvements to the system.

Possible future directions for this project include:
 - Benchmarking the LA Metro system against other transit systems worldwide. Open-sourcing our analysis is the first step towards beginning a discussion on how to measure and compare transit systems worldwide. Due to budget constraints and ageing infrastructure, perfect GPS tracking and precise reporting of arrival times is not commonly found in rail systems. We want to develop low-cost and reliable methods to estimate train arrival times at stations. 
 - Monitoring causes of delays and providing additional statistics on these.

### Non-Goals:
- Currently, monitoring the LA bus network is outside the scope of this project. 
- We do not plan to duplicate/compete with existing services that provide upcoming arrival predictions. NextBus, Google Maps and Transit already provide these services. We focus on historical data only.
 - We will not produce any new 'raw' data - for example like Transit's approach of gathering crowd-sourced positioning data from its users to support and improve Metro's predictions.

## Contact Us:

We have an ongoing discussion on the Hack For LA Slack. Sign up here: https://hackforla-slack.herokuapp.com/
Once you are signed up, click on "Channels" and search for '#metro-ontime' to join our chat.
We meet weekly on Tuesday nights at Hack For LA in Downtown Los Angeles. Details are here: http://www.hackforla.org/
You can also contact us via the issue tracker in this repository.

## Getting Started:

To run the python scripts we recommend using a virtual Python environment. 
The following example uses `venv` built into Python 3.
Run these commands to download and begin working with this repo:
```
git clone https://github.com/metro-ontime/performance_tracker.git
cd performance_tracker
python3 -m venv env
source env/bin/activate
pip install cython
pip install numpy
pip install pyproj
pip install -r requirements.txt
jupyter lab
```

Not all dependencies (cython and numpy) are included in requirements.txt since pip has issues installing all dependencies at once.

### General Workflow:

1. Run `log_job.sh` regularly over a time frame - say once per minute over 3 hours. See cron example further down in this README for details.
2. Run the scripts in `analyze_vehicle_positions.ipynb` to analyze the logs - setting the correct date and time based on the time frame logged.
3. Download a new schedule into data/GTFS by running:
    ```
    cd data/GTFS
    wget https://gitlab.com/LACMTA/gtfs_rail/raw/master/gtfs_rail.zip
    unzip gtfs_rail.zip
    ```
    **Note:** The schedule is updated daily (around 1am), so schedule data needs to redownloaded and parsed every day. Schedules are changed mainly due to track maintenance.

4. Run the schedule scripts in `schedule.ipynb`, also inputing the correct date and time frame.
5. Run the comparison scripts in `comparison.ipynb` - this will output a Marey diagram showing the tracked train positions alongside imaginary 'pace trains' following the schedule.

### Setup Git Hook (on deployment server):

There is a sample post-receive git hook in `performance-tracker/setup/post-receive.sample`.
Run the setup.sh script in that directory to copy it to your git hooks.

## Contributing:

The process for contributing to the performance tracker is as follows:
1. **Read** the currently open Issues to find out where we need help.
2. **Fork** this repository to your GitHub account.
3. **Discuss** with core contributors the feature you plan to add or bug you are tackling. You can have a conversation with us via the issue tracker OR on our Slack channel.
4. **Write** your code or documentation. Here is a Python style guide we try to follow: https://www.python.org/dev/peps/pep-0008/
5. **Push** your changes to your forked repository.
6. Make a **Pull Request** to this repository.

## This Repository:

- ./logger: class files for logging vehicle positions
- ./analyzer: class files for analyzing vehicle position data
- ./data: All data dumps and temporary log files.
- ./data/GTFS: LA Metro GTFS data is downloaded to this directory daily from their gitlab: https://gitlab.com/LACMTA/gtfs_rail

## Analysis Methodology:

LA Metro's real-time API (https://developer.metro.net/introduction/realtime-api-overview/) provides the "positions of Metro vehicles on their routes in real time." After some exploration of this API and also the NextBus real-time vehicle location API (also mentioned at that Metro developer webpage), we found that the NextBus data appears to be more accurate and up-to-date when polled more frequently (i.e. once per 60 seconds). We request the most recently reported location of all vehicles on a train line by making the following API call, where {line} is the train line number:

http://webservices.nextbus.com/service/publicJSONFeed?command=vehicleLocations&a=lametro-rail&r={line}

Our performance monitor logs the response of this API call, storing each vehicle's coordinates along with its direction, vehicle_id and the time of its last position update in a database. We then reconstruct each vehicle's journey and estimate the actual times that it arrived at each station, which we can then compare to the schedule. This process is not without flaws, so we are encouraging debate over how to improve our algorithms and measure train performance in a way that is most useful to riders. For example, a more useful metric of Metro performance for commuters might be the average wait time between services rather than strict adherence to scheduled arrival/departure times. Fortunately, we should be able to calculate several performance indicators from the tracking data, to provide a thorough picture of Metro performance.

## Notes on Time, Time Formats & Timezones

All stored DateTime objects should be in RFC3339 format, with the timezone set to UTC. We use the Pendulum library for Python to keep this consistent. Datetimes only need to be converted to local timezones on the front end. Metro's schedule data (from the GTFS) requires special treatment as one "day" is longer than 24 hours. Schedule trips have a "schedule_time" column - containing the original time as given by the GTFS file - and a "real_time" column - containing the datetime in RFC3339 UTC when that trip should occur.

## Train Tracking Logs

You can set up our logging script to track trains locally on any Unix machine running Python 3.6, SQLite3, and cron. 

### Example: set up train tracking every 1 minutes on Unix:
#### **Note:** We need to update this to work with the python virtual environment.

1. Edit crontab:
`*/1 * * * * cd path/to/this_directory && bash ./log_job.sh`
2. Start cron service:
`systemctl start cron`

Currently, you must edit log_job.sh to choose the line you wish to track - we will rewrite this to log all rail lines once we are ready to scale up.
