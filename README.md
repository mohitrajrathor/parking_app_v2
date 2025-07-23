# Parkly: Parking Facility Management App

### *Modern Application Development - II Project*

**Author:** Mohit Raj Rathor

---

## Overview

Parkly is a responsive multi-user web app for managing 4-wheeler parking lots. It supports real-time slot booking, user management, payments, reviews, and admin dashboards. The app is designed for both end-users and administrators to simplify parking operations.

---

## Tech Stack

* **Backend:** Flask, Flask-SQLAlchemy (SQLite), Celery, Redis
* **Frontend:** Vue.js, Bootstrap
* **APIs:** RESTful, secured with validation
* **Other Tools:** Leaflet (map view), OpenStreetMap API (address), Flask-Mail, Git

---

## Features

* User registration with email confirmation
* Admin dashboard with user and parking management
* Real-time slot booking via REST APIs
* Slot CRUD: add, update, delete, and manage availability
* Payments, reviews, and ratings
* html reports emailed to users/admin
* Daily & monthly jobs using Celery
* Frontend and backend data validation
* Map integration to show parking location
* Caching and background jobs with Redis


---

## Setup Instructions

+ ### Option 1: Bash (Linux/WSL only)

    ```bash
    git clone https://github.com/mohitrajrathor/parking_app_v2.git  
    cd parking_app_v2  

    chmod +x ./setup.sh  
    chmod +x ./run.sh  

    ./setup.sh      # Setup project  
    ./run.sh dev    # Start in dev mode  
    ```

    > **Note:** Requires Redis installed on your system.
    > SMTP email runs on `aiosmtpd` locally.

---

+ ### Option 2: Docker (Recommended)

    ```bash
    docker compose build --no-cache  
    docker compose up  
    ```

    > **Note:** Mailhog is used for email testing. No additional setup needed beyond Docker.

---
Feel free to contribute or raise issues via GitHub!