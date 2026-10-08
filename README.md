# Personal Trip & Expense Tracker API

## Problem Statement

Managing trips, travelers, and expenses manually can make it difficult to track
traveler capacity, overlapping trips, trip status, and budget usage.

This API provides a centralized way to manage trips, travelers, and expenses
while enforcing validation and business rules to keep the data consistent.

---
## Features

* Create and manage trips
* Update trips using `PUT`
* Update trip status using `PATCH`
* Delete trips
* Add travelers to trips
* Remove travelers from trips
* Prevent duplicate travelers in the same trip
* Prevent overlapping trips for the same traveler
* Enforce maximum traveler capacity
* Add expenses to trips
* Prevent expenses from exceeding the trip budget
* Generate trip summaries
* Validate request data
* Enforce trip lifecycle rules

---
## Prerequisites

- Python 3.10+
- Git
- pip
---
# Installation

## 1. Clone the repository

```bash
git clone https://github.com/Fail2/malay_chakma_trip_planner_batch_12.git
cd malay_chakma_trip_planner_batch_12
```

## 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

Activate it on Linux/macOS:

```bash
source venv/bin/activate
```

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

## 4. Run the application

```bash
python run.py
```

The API will run at:

```text
http://127.0.0.1:5000
```

---
## Run with run.sh

After cloning the repository:

```bash
chmod +x run.sh
./run.sh
```
---

# API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/trips/<trip_id>` | Get a trip |
| POST | `/api/v1/trips/` | Create a trip |
| PUT | `/api/v1/trips/<trip_id>` | Update a trip |
| DELETE | `/api/v1/trips/<trip_id>` | Delete a trip |
| PATCH | `/api/v1/trips/<trip_id>/status` | Update trip status |
| GET | `/api/v1/trips/<trip_id>/summary` | Get trip summary |
| POST | `/api/v1/trips/<trip_id>/travelers` | Add traveler |
| DELETE | `/api/v1/trips/<trip_id>/travelers/<traveler_id>` | Remove traveler |
| POST | `/api/v1/trips/<trip_id>/expenses` | Add expense |

# Tech Stack

* Python
* Flask
* Flask-SQLAlchemy
* SQLite
* REST API
* Git & GitHub

---

# Project Structure

```
malay_chakma_trip_planner_batch_12/
├── app/
|   ├── __init__.py
│   ├── models.py
│   ├── routes.py
│   └── services.py
├── instance/
│   └── trips.db
├── validators/
│   ├── expense_validator.py
│   ├── traveler_validator.py
│   └── trip_validator.py
├── .gitignore
├── config.py
├── README.md
├── requirements.txt
├── run.py
└── run.sh
```

---
## SQLite Database

The project uses SQLite as the database.

The database file is stored at:

```text
instance/trips.db
```
---
# API Base URL

```text
http://127.0.0.1:5000/api/v1/trips
```

---

# Trip API

## 1. Get Trip by ID

### Endpoint

```http
GET /api/v1/trips/<trip_id>
```

### Example

```http
GET /api/v1/trips/1
```

### Success Response

```json
{
    "success": true,
    "data": {
        "destination": "Cox's Bazar",
        "start_date": "2026-10-10",
        "end_date": "2026-10-15",
        "budget": 50000.0,
        "max_travelers": 5,
        "status": "PLANNED"
    }
}
```

---

## 2. Create Trip

### Endpoint

```http
POST /api/v1/trips/
```

### Request Body

```json
{
    "destination": "Cox's Bazar",
    "start_date": "2026-10-10",
    "end_date": "2026-10-15",
    "budget": 50000,
    "max_travelers": 5
}
```

### Validation Rules

* `destination` must be a string
* `destination` cannot be empty
* Maximum destination length is 100 characters
* Dates must use `YYYY-MM-DD`
* Trip dates cannot be in the past
* `end_date` must be later than `start_date`
* `budget` must be greater than 0
* `max_travelers` must be an integer greater than 0

### Success Response

```json
{
    "success": true,
    "message": "Trip created successfully",
    "data": {
        "id": 1,
        "destination": "Cox's Bazar"
    }
}
```

---

## 3. Update Trip

### Endpoint

```http
PUT /api/v1/trips/<trip_id>
```

### Example

```http
PUT /api/v1/trips/1
```

### Request Body

```json
{
    "destination": "Cox's Bazar",
    "start_date": "2026-10-10",
    "end_date": "2026-10-15",
    "budget": 60000,
    "max_travelers": 5
}
```

### Important

This endpoint follows `PUT` semantics, so all required trip fields must be provided.


For an `ongoing` trip, the following fields cannot be changed:

* destination
* start_date
* end_date
* budget
* max_travelers

---

## 4. Delete Trip

### Endpoint

```http
DELETE /api/v1/trips/<trip_id>
```

### Example

```http
DELETE /api/v1/trips/1
```

### Success Response

```json
{
    "success": true,
    "message": "Trip deleted successfully"
}
```

---

## 5. Update Trip Status

A dedicated status endpoint is available for changing only the trip status.

### Endpoint

```http
PATCH /api/v1/trips/<trip_id>/status
```

### Request Body

```json
{
    "status": "ongoing"
}
```

### Valid Statuses

```text
planned
ongoing
completed
cancelled
```

### Valid Transitions

```text
planned → ongoing
planned → cancelled

ongoing → completed
ongoing → cancelled
```

Completed and cancelled trips cannot be changed.

---

## 6. Get Trip Summary

### Endpoint

```http
GET /api/v1/trips/<trip_id>/summary
```

### Example

```http
GET /api/v1/trips/1/summary
```

### Response

```json
{
    "data": {
        "available_seats": 0,
        "budget": 35000.0,
        "destination": "Rangamati",
        "end_date": "2026-10-12",
        "expenses": {
            "items": [],
            "remaining_budget": 35000.0,
            "total": 0
        },
        "id": 1,
        "max_travelers": 1,
        "start_date": "2026-10-10",
        "status": "PLANNED",
        "travelers": {
            "items": [
                {
                    "email": "malay@example.com",
                    "id": 3,
                    "name": "Malay"
                }
            ],
            "traveler_count": 1
        }
    },
    "success": true
}
```

---

# Traveler API

## 7. Add Traveler to Trip

### Endpoint

```http
POST /api/v1/trips/<trip_id>/travelers
```

### Request Body

```json
{
    "name": "Rahim",
    "email": "rahim@gmail.com"
}
```

### Business Rules

* Traveler must have a valid name
* Traveler must have a valid email
* Email is used as traveler identity
* A traveler cannot be added twice to the same trip
* A trip cannot exceed `max_travelers`
* Travelers can only be added to `planned` trips
* Travelers cannot be added if the trip has already started
* A traveler cannot have another overlapping active trip
* Back-to-back trips are allowed

### Example

```text
Trip A: 2026-10-10 → 2026-10-15
Trip B: 2026-10-15 → 2026-10-20
```

The traveler can participate in both trips because the trips are back-to-back.

---

## 8. Remove Traveler from Trip

### Endpoint

```http
DELETE /api/v1/trips/<trip_id>/travelers/<traveler_id>
```

### Example

```http
DELETE /api/v1/trips/1/travelers/2
```

### Success Response

```json
{
    "success": true,
    "message": "Traveler removed from <Trip> successfully"
}
```

This removes the traveler from the trip relationship.

It does **not** delete the Traveler record itself.

---

# Expense API

## 9. Add Expense to Trip

### Endpoint

```http
POST /api/v1/trips/<trip_id>/expenses
```

### Request Body

```json
{
    "title": "Hotel",
    "amount": 15000,
    "description": "Hotel booking for five nights"
}
```

### Business Rules

* `title` must be a string
* `title` cannot be empty
* Maximum title length is 50 characters
* `amount` must be a valid positive number
* `description` must be a string
* `description` cannot be empty
* Maximum description length is 200 characters
* Expenses can only be added to `planned` or `ongoing` trips
* Total expenses cannot exceed the trip budget
* Spending the exact remaining budget is allowed
* `completed` and `cancelled` trips cannot accept expenses

### Example

```text
Trip budget = 50,000
Existing expenses = 40,000
New expense = 10,000
```

Result:

```text
40,000 + 10,000 = 50,000
```

The expense is allowed.

But:

```text
40,000 + 10,001 = 50,001
```

The expense is rejected.

---

# HTTP Status Codes

| Status | Meaning                        |
| ------ | ------------------------------ |
| 200    | Request successful             |
| 201    | Resource created               |
| 400    | Validation/business rule error |
| 404    | Resource not found             |
| 409    | Conflict                       |
| 500    | Internal server error          |

---

# Main Business Rules

## Trip Rules

1. Trip `end_date` must be later than `start_date`.
2. Budget must be greater than 0.
3. `max_travelers` must be greater than 0.
4. Trip status transitions must follow the defined lifecycle.
5. Completed trips cannot be edited.
6. Cancelled trips cannot be edited.

## Traveler Rules

1. A traveler cannot be added twice to the same trip.
2. A trip cannot exceed its maximum traveler capacity.
3. Travelers can only be added to planned trips.
4. Travelers cannot be added after the trip has started.
5. A traveler cannot have overlapping active trips.
6. Back-to-back trips are allowed.

## Expense Rules

1. Expense amount must be greater than 0.
2. Expense amount must be a valid finite number.
3. Total expenses cannot exceed the trip budget.
4. Exact budget usage is allowed.
5. Expenses can only be added to planned or ongoing trips.

---

# Data Relationships

The project uses SQLAlchemy relationships.

### Trip → Expense

One Trip can have many Expenses.

```text
Trip
 │
 ├── Expense
 ├── Expense
 └── Expense
```

### Trip ↔ Traveler

Trips and Travelers have a many-to-many relationship.

```text
Trip
 │
 ├── Traveler
 ├── Traveler
 └── Traveler
```

A traveler can also belong to multiple trips as long as the active trip dates do not overlap.

---

# Testing

The API can be tested using:

* Postman
* Insomnia
* curl

Recommended testing order:

```text
1. Create Trip
2. Get Trip
3. Add Traveler
4. Add Expense
5. Get Trip Summary
6. Update Trip Status
7. Remove Traveler
8. Delete Trip
```

---

# Important Edge Cases Tested

The project handles several important edge cases:

* **Completed/cancelled trips** are excluded from traveler overlap checks
* Max travelers can't be less than **current travelers in trip**
* Budget can't be less than **current total expenses**
* **NaN**/infinite expense amounts are rejected
* Duplicate traveler in the same trip is rejected
* Trip capacity is enforced
* Overlapping active trips for the same traveler are rejected
* Back-to-back trips are allowed
* Exact budget usage is allowed
* Expenses exceeding the budget are rejected
* Completed/cancelled trips cannot accept expenses
* Completed/cancelled trips cannot be modified

---
# SQLite Initialization and Storage

* The application uses SQLite as its database, with Flask-SQLAlchemy handling the database models and relationships.
* Database tables are created automatically when the application starts, so no manual database setup is required.
* The SQLite database file is stored locally at `instance/trips.db`.
* The database file is generated locally and is excluded from the repository.
* Since the data is stored in a persistent SQLite database, it remains available after the application is restarted.


# Known Limitations

* SQLite is intended for local development and small-scale usage.
* Authentication and authorization are not implemented.
* Trip status is automatically updated based on trip dates:

  * When the trip start date is reached, the status becomes `ONGOING`.
  * When the trip end date is reached, the status becomes `COMPLETED`.

---

