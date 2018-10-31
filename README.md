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

## For Contributors:

What We Need:
 - Programmers with Python/GIS/Pandas or related experience
 - Front End Developers (React, D3)
 - QA Testers (spotting bugs, feedback on site-design -- currently low priority)

This web application is built on a python backend, which logs and processes vehicle tracking data from Metro's real-time API. The front end is a React app hosted on a static server (GitHub or Netlify - TBC) that is recompiled daily as new performance data becomes available on our python backend. 

Please see the repo "Issues" tab for currently open tickets.

## Progress Report:

### Step 1: Research Data Landscape
#### Progress
Largely complete
#### Summary
The primary source of Metro data, naturally, is Metro's publicly released data sets and API endpoints. Metro partners with NextBus to produce predictions and real-time data, releases regular performance reports and responds to FOIA requests. All media coverage of Metro performance is based on these primary sources to our knowledge. The ONLY external primary data we are aware of is Transit's crowd-sourced data, which is incomplete.

### Step 2: Request Inaccessible Data
#### Progress
In progress
#### Summary
We are in contact with Metro staff and developers, aiming to set up a meeting to discuss key questions and datasets. We have also submitted an FOIA request to Metro for raw arrival time records, should they exist. Transit is unable to provide us with historical crowd-sourced records. 
### Step 3: Define Data
#### Progress
Started
#### Summary
We have a good understanding of the Metro API and datasets, but need to produce our own documentation and data dictionary so that contributors have an easy reference for all input data.
### Step 4: Define Tests, Basemodels, Model Inputs and Outputs
#### Progress
Beginning
#### Summary
We have a good idea of what the model inputs and outputs should be (again, these need to be documented). The most difficult part of the entire project, however, will be to define the arrival estimate model. The timing of vehicle position updates are NOT in sync with the train schedule, hence we cannot directly know the actual arrival times of Metro trains. Instead, we need to determine whether trains are running to schedule based on an arbitrary set of GPS coordinates and times for each trip. 
### Step 5: Run Models
#### Progress
Beginning
#### Summary
Our initial logging scripts are working - regularly inserting vehicle tracking data into a SQLite database. We need to continue to build out this system and transition over to a dedicated server running Postgres.
### Step 6: Report/Visualize the data
#### Progress
Not started
#### Summary
We need to build a website frontend to report our statistics. The current plan is a React app running on a static hosting service (GitHub or Netlify) - this should be easy to build and cheap to maintain.
### Step 7: Maintain Information/Track Usage Metrics
#### Progress
Not started
#### Summary
Once we get underway building the frontend, we will build in analytics to measure the success and popularity of our app.

## Research:

Please refer to the file ./Data_Catalog in this repository for a summary of data sources and research articles relevant to understanding the Metro API and our monitoring process. 

## Analysis Methodology:

LA Metro's real-time API (https://developer.metro.net/introduction/realtime-api-overview/) provides the "positions of Metro vehicles on their routes in real time." Our peformance monitor logs the output of this API, storing each vehicle's coordinates along with its direction, vehicle_id and the time of its last position update in a database (PostgreSQL - TBC). We then reconstruct each vehicle's journey and estimate the actual times that it arrived at each stop, which we can then compare to the schedule. This process is not without flaws, so we are encouraging debate over how to improve our algorithms and measure train performance in a way that is most useful to riders. For example, depending on the time of day, a more useful metric of Metro performance might be the average wait time between services. If trains are not strictly following the schedule but are running relatively frequently - does that matter to riders?

Our understanding of Metro's current reporting system for measuring late arrivals is this:
Any train arriving at a station more than FIVE minutes after it is scheduled is recorded manually by Metro staff. 

At peak times when trains might be running 5 or 6 minutes apart - they could simply disregard the schedule and still claim 100% on time arrivals. This is one reason we believe that a more transparent and precise performance measurement tool would be valuable.

## This Repository:

./App: Contains our logging application and database analysis. 

./GTFS: Relevant static data - stops & schedule info

Tracking_Data_Rough_Analysis.ipynb: Analysis of vehicle GPS updates and their frequency, geographic distribution. Here we are trying to determine how the positioning system works in order to better inform our arrival time estimations.
Requires: Jupyter Notebook (Anaconda)

distance_calculations.qgz: QGIS project mapping all the points and lines - we will use this to get an accurate calculation of distances between stations. Should be able to line up vehicle coordinates with the shapefiles.
Requires: QGIS (https://qgis.org/en/site/)

## Train Tracking Logs

You can set up our logging script to track trains locally on any Unix machine running Python 3.6, SQLite3, and cron. 

### Example: set up train tracking every 1 minutes on Linux:

1. Edit crontab:
`*/1 * * * * cd path/to/this_directory && bash ./log_job.sh`
2. Start cron service:
`systemctl start cron`

Currently, you must edit log_job.sh to choose the line you wish to track - we will rewrite this to log all rail lines once we are ready to scale up.
