#!/bin/sh

# Ensure log file exists
touch /home/dayat/LAB/PYTHON/playground/logs.log

# Set up cron job to run clean_up.py every hour
echo '0 * * * * /home/dayat/LAB/PYTHON/playground/.env/bin/python /home/dayat/LAB/PYTHON/playground/clean_up.py >> /home/dayat/LAB/PYTHON/playground/logs.log 2>&1' > /home/dayat/LAB/PYTHON/playground/cron
crontab /home/dayat/LAB/PYTHON/playground/cron

# Start the Django development server
/home/dayat/LAB/PYTHON/playground/.env/bin/python /home/dayat/LAB/PYTHON/playground/manage.py runserver 0.0.0.0:1997
