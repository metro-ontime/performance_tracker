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

