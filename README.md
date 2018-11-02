# Metro Performance Monitor

### A Health App for the Los Angeles Metro Rail system

This website, incubated at Hack for LA, tracks LA Metro trains and provides up to date statistics summarizing daily, weekly, monthly and annual performance. Our mission is to monitor and report the number of both on-time and late train arrivals on an ongoing basis for all Metro rail lines in Los Angeles. These are:
 - Blue Line
 - Red Line
 - Green Line
 - Gold Line
 - Purple Line
 - Expo Line

By publishing these statistics and open-sourcing our methodology, we aim to give riders an accurate and unvarnished picture of the system's state over time. Hopefully, this will correct any public misperception of Metro's track record and help inform decision-makers when assessing future improvements to the system.

Possible future directions for this project include:
 - Benchmarking the LA Metro system against other transit systems worldwide. Open-sourcing our analysis is the first step towards beginning a discussion on how to measure and compare transit systems worldwide. Due to budget constraints and ageing infrastructure, perfect GPS tracking and precise reporting of arrival times is not commonly found in rail systems. We want to develop low-cost and reliable methods to estimate train arrival times at stations. 
 - Monitoring causes of delays and providing additional statistics on these.

### Non-Goals:
- Currently, monitoring the LA bus network is outside the scope of this project. 
- We do not plan to duplicate/compete with existing services that provide upcoming arrival predictions. NextBus, Google Maps and Transit already provide these services. We focus on historical data only.
 - We will not produce any new 'raw' data - for example like Transit's approach of gathering crowd-sourced positioning data from its users to support and improve Metro's predictions.

# For Contributors:
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
pip install -r requirements.txt
jupyter lab
```

## This Repository:

- ./logger: class files for logging vehicle positions
- ./analyzer: class files for analyzing vehicle position data
- ./data: All data dumps and temporary log files.
- ./data/GTFS: LA Metro GTFS data is downloaded to this directory daily from their gitlab: https://gitlab.com/LACMTA/gtfs_rail

## Analysis Methodology:

LA Metro's real-time API (https://developer.metro.net/introduction/realtime-api-overview/) provides the "positions of Metro vehicles on their routes in real time." Our performance monitor logs the output of this API, storing each vehicle's coordinates along with its direction, vehicle_id and the time of its last position update in a database (PostgreSQL - TBC). We then reconstruct each vehicle's journey and estimate the actual times that it arrived at each stop, which we can then compare to the schedule. This process is not without flaws, so we are encouraging debate over how to improve our algorithms and measure train performance in a way that is most useful to riders. For example, depending on the time of day, a more useful metric of Metro performance might be the average wait time between services. If trains are not strictly following the schedule but are running relatively frequently - does that matter to riders?

Our understanding of Metro's current reporting system for measuring late arrivals is this:
Any train arriving at a station more than FIVE minutes after it is scheduled is recorded manually by Metro staff. 

At peak times when trains might be running 5 or 6 minutes apart - they could simply disregard the schedule and still claim 100% on time arrivals. This is one reason we believe that a more transparent and precise performance measurement tool would be valuable.

## Train Tracking Logs

You can set up our logging script to track trains locally on any Unix machine running Python 3.6, SQLite3, and cron. 

### Example: set up train tracking every 1 minutes on Linux:
#### **Note:** We need to update this to work with the python virtual environment.

1. Edit crontab:
`*/1 * * * * cd path/to/this_directory && bash ./log_job.sh`
2. Start cron service:
`systemctl start cron`

Currently, you must edit log_job.sh to choose the line you wish to track - we will rewrite this to log all rail lines once we are ready to scale up.
