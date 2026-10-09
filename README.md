# Modern Application Development Project - Vehicle Parking App V1

A multi-user web application for managing 4-wheeler parking lots, parking spots, and reservations.

## Overview

The app has two roles:

**Admin (superuser)**: created automatically when the database is first initialised; no registration needed. Manages parking lots and monitors usage.

**User**: registers and logs in, books a spot in a lot, and releases it when leaving.

Spots are auto-allocated (first available spot in the chosen lot). Users cannot pick a spot manually.

## Features

**Admin**
- Log in and view the dashboard
- Create parking lots; the spots are generated automatically from the lot's maximum number of spots
- Edit lot details (location, address, pincode, price, landmark)
- Delete a lot only when none of its spots are occupied
- View each lot's spots and the booking details for any occupied spot
- Mark a free spot as unavailable, or make it available again
- View all registered users and all bookings
- Search users by ID, or lots by location
- View summary charts for revenue per lot and spot occupancy per lot
- View and edit the admin profile

**User**
- Register and log in
- Search parking lots by location or pincode
- Book a spot by entering the vehicle number
- Release the spot when leaving; the cost is calculated from the parked time and the lot's hourly price
- View booking history on the dashboard
- View summary charts for monthly spending and spending per lot
- View and edit the profile

## Tech Stack

- **Backend:** Flask, Flask-SQLAlchemy
- **Frontend:** Jinja2 templates, HTML, CSS, Bootstrap 5
- **Charts:** Chart.js
- **Database:** SQLite (tables are created programmatically with SQLAlchemy)

## Database Tables

- **Admin**: username and password
- **User**: username, password hash, full name, address, pincode
- **Parking_lot**: location, address, pincode, price, maximum spots, landmark
- **Parking_spot**: belongs to a lot; booked or free; optional status note (e.g. unavailable)
- **Booking**: links a user to a spot, with vehicle number, start time, end time, and cost

## Project Structure

    vehicle-parking-v1/
    ├── app.py                  # App setup and entry point
    ├── requirements.txt
    ├── applications/
    │   ├── models.py           # Database models
    │   └── routes.py           # All routes (admin and user)
    ├── templates/
    │   ├── base.html
    │   ├── login.html
    │   ├── register.html
    │   ├── home.html
    │   ├── admin/              # Admin pages
    │   └── user/               # User pages
    └── instance/
        └── my_db.sqlite3       # SQLite database


