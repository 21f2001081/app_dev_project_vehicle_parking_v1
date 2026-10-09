# Modern Application Development Project - Vehicle Parking App V1

A multi-user web application for managing 4-wheeler parking lots, parking spots, and reservations.

## Overview

The app has two roles:

**Admin (superuser)**: created automatically when the database is first initialised; no registration needed. Manages parking lots and monitors usage.
**User**: registers and logs in, books a spot in a lot, and releases it when leaving.

Spots are auto-allocated (first available spot in the chosen lot). Users cannot pick a spot manually.

## Features

**Admin**
- Log in with pre-seeded superuser credentials
- Create, edit, and delete parking lots (delete only if every spot is empty)
- Spots are generated automatically from a lot's maximum spot count; increasing or decreasing the count adds or removes spots
- View the status of every spot (Available / Occupied) and the parked vehicle's details for occupied spots
- View all registered users
- View summary charts for lots and spots

**User**
- Register and log in
- Choose an available parking lot; the app allots the first free spot
- Mark the spot as occupied once parked, and release it on exit
- Parking and leaving timestamps are recorded; cost is computed from duration and the lot's price
- Personal parking history and summary charts

## Tech Stack

- **Backend:** Flask (Python)
- **Frontend:** Jinja2, HTML, CSS, Bootstrap
- **Database:** SQLite (created programmatically)

## Database Tables

- **User**: account details and role
- **ParkingLot**: location name, price, address, pin code, maximum spots
- **ParkingSpot**: belongs to a lot, status (Available / Occupied)
- **Reservation**: links a user to a spot, with parking time, leaving time, and cost
