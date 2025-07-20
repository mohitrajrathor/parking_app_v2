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


# run all searvices
# ./run.sh production

echo "setup completed."