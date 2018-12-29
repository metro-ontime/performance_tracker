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

We have a development environment setup that runs Jupyter Lab inside a Docker container. 
If you want to play around with the code interactively and test out code before converting it to python scripts,
the Jupyter Lab environment is ideal. To get it running, execute the following:
```
git clone https://github.com/metro-ontime/performance_tracker.git
cd performance_tracker/dev
bash build.sh <YOUR USERNAME>
cd ..
bash start-dev.sh <YOUR USERNAME>
```
The Jupyter server will provide a token - copy this to your clipboard.
Then open a browser window and navigate to:
`localhost:8888/?token=<YOUR TOKEN>`
This will open Jupyter Lab and give you access to all the files in this repo. 
All file changes will be saved even after the Docker container is destroyed.

### How the App Works:

The app is a set of python scripts (located at `performance_tracker/performance_tracker`), which run at varying intervals. 
You may run these either manually or via a cronjob. The following example uses `query_vehicles.sh`.
If we want to get the current location of vehicles on a line, from the repo root directory we execute:
```
performance_tracker/query_vehicles.sh <YOUR USERNAME> $(pwd)
```

The username argument is necessary to ensure Docker runs as your user and not as root.
Now if you go to `./performance_tracker/data/vehicle_tracking/raw` you will see the files that have been created for each line.
You can set up a cronjob easily to pull vehicle location data on a schedule. A cronjob set to get data every minute will follow this template:
```
*/1 * * * * bash path/to/this_repository/performance_tracker/query_vehicles.sh <YOUR USERNAME> path/to/this_repository
```

### Setting up a server with git hook:

You can easily setup a server to run this app. This example assumes the server username is 'ubuntu'.
1. SSH into your server.
2. Install Docker (https://docs.docker.com/install/overview/)
3. Enable cron service
`systemctl start cron`
4. Clone this repo:
`git clone https://github.com/metro-ontime/performance_tracker.git`
5. Execute setup script
```
cd performance_tracker/performance_tracker/setup
bash setup.sh
```
6. Then on your local machine add the server git directory (performance_tracker-gitdir) as a git remote.
```
git remote add production <YOUR SERVER SSH ALIAS>:~/performance_tracker-gitdir
```
7. Push master to production:
`git push production master`

This should execute the Docker build script and set the cronjob correctly.


## Contributing:

The process for contributing to the performance tracker is as follows:
1. **Read** the currently open Issues to find out where we need help.
2. **Fork** this repository to your GitHub account.
3. **Discuss** with core contributors the feature you plan to add or bug you are tackling. You can have a conversation with us via the issue tracker OR on our Slack channel.
4. **Write** your code or documentation. Here is a Python style guide we try to follow: https://www.python.org/dev/peps/pep-0008/
5. **Push** your changes to your forked repository.
6. Make a **Pull Request** to this repository.

## Analysis Methodology:

LA Metro's real-time API (https://developer.metro.net/introduction/realtime-api-overview/) provides the "positions of Metro vehicles on their routes in real time." After some exploration of this API and also the NextBus real-time vehicle location API (also mentioned at that Metro developer webpage), we found that the NextBus data appears to be more accurate and up-to-date when polled more frequently (i.e. once per 60 seconds). We request the most recently reported location of all vehicles on a train line by making the following API call, where {line} is the train line number:

http://webservices.nextbus.com/service/publicJSONFeed?command=vehicleLocations&a=lametro-rail&r={line}

Our performance monitor logs the response of this API call, storing each vehicle's coordinates along with its direction, vehicle_id and the time of its last position update in a database. We then reconstruct each vehicle's journey and estimate the actual times that it arrived at each station, which we can then compare to the schedule. This process is not without flaws, so we are encouraging debate over how to improve our algorithms and measure train performance in a way that is most useful to riders. For example, a more useful metric of Metro performance for commuters might be the average wait time between services rather than strict adherence to scheduled arrival/departure times. Fortunately, we should be able to calculate several performance indicators from the tracking data, to provide a thorough picture of Metro performance.

## Notes on Time, Time Formats & Timezones

All stored DateTime objects should be in RFC3339 format, with the timezone set to UTC. We use the Pendulum library for Python to keep this consistent. Datetimes only need to be converted to local timezones on the front end. Metro's schedule data (from the GTFS) requires special treatment as one "day" is longer than 24 hours. Schedule trips have a "schedule_time" column - containing the original time as given by the GTFS file - and a "real_time" column - containing the datetime in RFC3339 UTC when that trip should occur.
