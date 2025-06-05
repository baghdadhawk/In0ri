#!/bin/bash

service cron start

# Persist MongoDB credentials for the app processes
export MONGODB_USERNAME=${MONGODB_USERNAME}
export MONGODB_PASSWORD=${MONGODB_PASSWORD}
export MONGODB_HOSTNAME=${MONGODB_HOSTNAME}

python3 /opt/In0ri/FlaskApp/app.py &
exec python3 /opt/In0ri/api.py
