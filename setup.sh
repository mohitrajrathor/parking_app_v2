#!/bin/bash



# check for existence of backend and frontend directories
if [ ! -d "backend" ]; then
  echo "[files check] Backend directory does not exist. Please create it."
  exit 1
fi

if [ ! -d "frontend" ]; then
    echo "[files check] frontend directory does not exist. please create it."
    exit 1
fi



# check if .venv exsists in current directory
if [ ! -d ".venv" ]; then
    echo "[venv] Creating virtual environment..."
    python3 -m venv .venv
    echo "[venv] Virtual environment created."
else
    echo "[venv] Virtual environment already exists."
fi



# activate the virtual environment
source .venv/bin/activate
echo "[venv] Virtual environment activated."



# install backend dependencies
if [ -f "backend/requirements.txt" ]; then
    echo "[venv] Installing backend dependencies..."
    pip install -r backend/requirements.txt
    echo "[venv] Backend dependencies installed."
else
    echo "[venv] No requirements.txt found in backend directory."
    exit 1
fi



# install frontend dependencies
if [ -f "frontend/package.json" ]; then
    echo "[frontend] Installing frontend dependencies..."
    cd frontend
    npm install
    echo "[frontend] Frontend dependencies installed."
    cd ..
else
    echo "[frontend] No package.json found in frontend directory."
    exit 1
fi

if [ -d "frontend/dist" ]; then
    echo "[frontend] Removing existing dist directory..."
    rm -rf frontend/dist
    echo "[frontend] Existing dist directory removed."
    cd frontend
    echo "[frontend] Building frontend..."
    npm run build
    echo "[frontend] Frontend build completed."
    cd ..
fi



# run database migrations 
if [ ! -d "backend/instance" ]; then
    echo "[backend] Initializing database..."
    cd backend
    flask db init
    echo "[backend] Database initialized."
    flask db migrate
    flask db upgrade
    echo "[backend] Database migrations completed."
    cd ..
elif [ -d "backend/migrations" ]; then
    echo "[backend] Running existing database migrations..."
    cd backend
    flask db upgrade
    echo "[backend] Database migrations completed."
    cd ..
else
    echo "[backend] No migrations directory found in backend."
fi


# check if redis is installed
if ! command -v redis-server &> /dev/null; then
    echo "[redis] Redis server is not installed, installing Redis..."
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        sudo apt-get update
        sudo apt-get install redis-server -y
    fi 
    echo "[redis] Redis server installed."
fi


# Start redis in background
if ! pgrep -x "redis-server" > /dev/null; then
    echo "[redis] Starting Redis server..."
    redis-server --daemonize yes &
    echo "[redis] Redis server started."
else
    echo "[redis] Redis server is already running."
fi

# Start aiosmtpd in background
if ! pgrep -f "aiosmtpd" > /dev/null; then
    echo "[aiosmtpd] Starting aiosmtpd server..."
    python -m aiosmtpd -n -l localhost:1025 --debug &
    echo "[aiosmtpd] aiosmtpd server started on port 1025."
else
    echo "[aiosmtpd] aiosmtpd server is already running."
fi

# Start flask app in foreground (last, so script doesn't exit)
echo "[backend] Starting the application..."
cd backend
(flask run --port 1234 --debug) & (celery -A celery_worker worker --loglevel=info) & (celery -A celery_worker beat --loglevel=info)
echo "[backend] Application started on port 1234."



