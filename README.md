# Parkly: Parking Facility Management App

### *Modern Application Development - II Project*

**Author:** Mohit Raj Rathor

---

## Overview

Parkly is a responsive multi-user web app for managing 4-wheeler parking lots. It supports real-time slot booking, user management, payments, reviews, and admin dashboards. The app is designed for both end-users and administrators to simplify parking operations.

---

## Demo Screenshots

<div align="center">

<img src="media/Home-demo.png" alt="Home Page Demo" width="500" style="border-radius: 10px; box-shadow: 0 2px 8px #ccc; margin-bottom: 16px;"/>

<br/>

<table>
    <tr>
        <td align="center" style="padding: 12px;">
            <img src="media/Home-demo.png" alt="Home Page Demo" width="300" style="border-radius: 8px; box-shadow: 0 1px 6px #bbb;"/><br/>
            <b>Home Page</b>
        </td>
        <td align="center" style="padding: 12px;">
            <img src="media/User-demo.png" alt="User Dashboard Demo" width="300" style="border-radius: 8px; box-shadow: 0 1px 6px #bbb;"/><br/>
            <b>User Dashboard</b>
        </td>
    </tr>
</table>

</div>

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

## Database Details

The application uses **SQLite** as the primary database, managed via **Flask-SQLAlchemy**. The schema is designed to support users, parking slots, bookings, payments, reviews, and admin operations. Relationships are normalized for efficient queries and data integrity.

### Entity-Relationship (ER) Diagram

Below is the ER diagram representing the database schema:

![Database ER Diagram](media/ER_Diagram.png)


---

## Setup Instructions
+ ### Create .env file and copy paste the following for development.
    add following to root directory of the project.
    ```env
    secret_key=dsvrwsg8v4654vr6rs5gdsvc5746dnivegkl3905u480ei
    mail_server=localhost
    mail_port=1025
    ```

    add following to frontend/ dir.
    ```env
    # frontend
    VITE_BASE_URL=http://localhost:1234
    ```



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