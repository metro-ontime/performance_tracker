#!/bin/bash

#This script is intended to automatically configure new EC2 instances on launch. To make use of it; copy the contents to your clipboard, log-in to the AWS console, select EC2, and click on 
#the "launch template" option in the left-hand navigation pane. Make sure you are using the Ubuntu 18.04 AMI (with a t2.micro instance if you want to stay within the bounds of free tier), and scroll down
#to advanced details. Click the dropdown, and paste the contents of this file you previously copied into user data, and click "create template version." You will now be able to launch new instances with
#this template via the launch instances drop down on the EC2 dashboard.
IMAGE="<image name>"
#Install Docker
(
set -e
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
docker pull "$IMAGE"
set +e
)

#Create .env, edit as necessary
mkdir /home/ubuntu/docker_config && cat > /home/ubuntu/docker_config/.env <<EOF
LOCAL_DATA=/app/data
DATASTORE_NAME=S3
DATASTORE_PATH=performance-tracker-test
TMP_DIR=/app/data/tmp
METRO_LINES=801,802,803,804,805,806
METRO_AGENCY=lametro-rail
TIMEZONE=America/Los_Angeles
SCHEDULE_URL=https://gitlab.com/LACMTA/gtfs_rail/raw/master/gtfs_rail.zip
VEHICLE_API_URL=http://webservices.nextbus.com/service/publicJSONFeed
LOG_TIMESTAMPS=TRUE
AWS_ACCESS_KEY_ID=<access key id>
AWS_SECRET_ACCESS_KEY=<secret key>
EOF

#allow for timestamps on STDERR

(
set -e
mkdir /home/ubuntu/utils

cat > /home/ubuntu/utils/timestamp_errors.sh <<EOF
#!/bin/bash
while read -r line; do
   echo "[\$(date +%Y-%m-%d\ %H:%M:%S)] \$line" >> /home/ubuntu/logs/errors.log
done
EOF
chmod 755 /home/ubuntu/utils/timestamp_errors.sh
chown -R ubuntu /home/ubuntu/utils
set +e
)

#Create Shell Scripts
mkdir /home/ubuntu/logs
touch /home/ubuntu/logs/errors.log
touch /home/ubuntu/logs/output.log
chown -R ubuntu /home/ubuntu/logs 

(
set -e
cat > /home/ubuntu/daily_at_2.sh <<EOF
#!/bin/bash
sudo docker run --rm --env-file /home/ubuntu/docker_config/.env -v /home/ubuntu/data/tmp:/app/data/tmp "$IMAGE" bash ./tasks/DAILY_AT_2AM.sh
EOF
chmod 755 daily_at_2.sh
set +e
)

(
set -e
cat > /home/ubuntu/every_minute.sh <<EOF
#!/bin/bash
sudo docker run --rm --env-file /home/ubuntu/docker_config/.env -v /home/ubuntu/data/tmp:/app/data/tmp "$IMAGE" bash ./tasks/EVERY_MINUTE.sh
EOF
chmod 755 every_minute.sh
set +e
)

#run the EVERY_15_MIN tasks every hour in dev to reduce the amount of writes to S3 (free tier caps at 2k per month) 
(
set -e
cat > /home/ubuntu/every_hour.sh <<EOF
#!/bin/bash
sudo docker run --rm --env-file /home/ubuntu/docker_config/.env -v /home/ubuntu/data/tmp:/app/data/tmp "$IMAGE" bash ./tasks/EVERY_15_MINS.sh
EOF
chmod 755 every_hour.sh
set +e
)

#Configure cron tasks

(
set -e
cat > every_minute <<EOF
CRON_TZ=UTC
* * * * * root /home/ubuntu/every_minute.sh 2> >(/home/ubuntu/utils/timestamp_errors.sh) >> /home/ubuntu/logs/output.log
EOF
chmod 644 every_minute
mv every_minute /etc/cron.d
set +e
)

(
set -e
cat > every_hour <<EOF
CRON_TZ=UTC
0 * * * * root /home/ubuntu/every_hour.sh 2> >(/home/ubuntu/utils/timestamp_errors.sh) >> /home/ubuntu/logs/output.log 
EOF
chmod 644 every_hour
mv every_hour /etc/cron.d
set +e
)

(
set -e
cat > every_day <<EOF
CRON_TZ=UTC
* 11 * * * root rm -rf ~/data/tmp && /home/ubuntu/daily_at_2.sh 2> >(/home/ubuntu/utils/timestamp_errors.sh) >> /home/ubuntu/logs/output.log
EOF
chmod 644 every_day
mv every_day /etc/cron.d
set +e
)

#run the daily script once on launch to obtain schedule for current day
bash /home/ubuntu/daily_at_2.sh 2> >(/home/ubuntu/utils/timestamp_errors.sh) >> /home/ubuntu/logs/output.log
