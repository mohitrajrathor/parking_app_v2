#!/bin/bash

if [[ ! "$1" ]]; then
    echo "development choice is not given, aborting..."
    exit 1
fi

if [ ! -d ".venv" ]; then 
    echo "virtual env not found, aborting..."
    exit 1
fi

if [ ! -d "backend" ]; then
    echo "backend dir not exist!"
    echo "aborting..."
    exit 1
fi

if [ ! -d "backend/app" ]; then
    echo "app dir does not exist, aborting..."
    exit 1
fi

if [ ! -f "backend/celery_worker.py" ]; then
    echo "celery_worker.py not exist, aborting..."
    exit 1
fi

echo "File check complete."
echo "Starting application..."


if [ -d ".venv" ]; then
    echo "Activating virtual enviroment..."
    source .venv/bin/activate
    echo "[venv] Virtual environment activated."
else
    echo "virtual enviroment not found creating..."
    python3 -m venv .venv
    source .venv/bin/activate
    python -m pip install -r backend/requirements.txt
fi


# Trap function to stop all background processes
stop_all() {
    echo "Stopping all processes..."
    kill $PID1 $PID2 $PID3 $PID4 $PID5 $PID6 2>/dev/null
    exit
}

trap stop_all SIGINT

# Start backend services
cd backend
aiosmtpd -n -l localhost:1025 --debug &
PID1=$!

redis-server &
PID2=$!

celery -A celery_worker worker -l INFO &
PID3=$!

celery -A celery_worker beat -l INFO &
PID4=$!



# Conditional dev or production
if [[ "$1" == "dev" ]]; then
    (cd ../frontend && npm run dev) &
    PID5=$!
    (cd ../backend && flask run --port 1234 --debug) &
    PID6=$!
    wait $PID1 $PID2 $PID3 $PID4 $PID5 $PID6
else
    PID5=0
    flask run --port 1234 --debug &
    PID6=$!
    wait $PID1 $PID2 $PID3 $PID4 $PID6
fi
