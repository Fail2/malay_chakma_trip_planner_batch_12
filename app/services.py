from flask import jsonify

from app.models import Trip, Traveler, Expense
from app import db
from datetime import datetime, date
from validators.traveler_validator import traveler_create_validate
from validators.expense_validator import expense_create_validate
from validators.trip_validator import trip_create_validate, trip_update_validate, trip_status_update_validate


# Trip Service Part-----------------------------------------------

def list_trips():
    trips = Trip.query.all()
    return {
        "success": True,
        "data":[
            {
                "id": trip.id, "destination": trip.destination, 
                "start_date": trip.start_date.isoformat(),
                "end_date": trip.end_date.isoformat(),
                "budget": trip.budget, "max_travelers": trip.max_travelers, 
                "status": trip.status
            } 
            for trip in trips
        ]
    }, 200


def get_trip(trip_id):
    trip = Trip.query.get(trip_id)

    if not trip:
        return {
            "success": False,
            "error": "Resource not found",
            "message": f"Trip with ID {trip_id} does not exist",
        },404

    return {
        "success": True,
        "data": {"id": trip.id,"destination": trip.destination, "start_date": trip.start_date.isoformat(), 
        "end_date": trip.end_date.isoformat(), "budget": trip.budget, 
        "max_travelers": trip.max_travelers, "status": trip.status}
        }, 200


def create_trip(data):
    msg, is_error, cleaned_data = trip_create_validate(data)

    if is_error:
        return {
            "success": False,
            "error": "Validation error",
            "message": msg
        },400

    trip = Trip(
        destination = cleaned_data['destination'],
        start_date = cleaned_data['start_date'],
        end_date = cleaned_data['end_date'],
        budget = cleaned_data['budget'],
        max_travelers = cleaned_data['max_travelers']
    )

    db.session.add(trip)
    db.session.commit()

    return {
        "success": True,
        "message": "Trip created successfully",
        "data": {
            "id": trip.id,
            "destination": trip.destination,
            "start_date": trip.start_date.isoformat(),
            "end_date": trip.end_date.isoformat(),
            "budget": trip.budget,
            "max_travelers": trip.max_travelers,
            "status": trip.status
        }
    }, 201


def update_trip(trip_id, data):
    trip = Trip.query.get(trip_id)

    if not trip:
        return {
            "success": False,
            "error": "Resource not found",
            "message": f"Trip with ID {trip_id} does not exist",
        },404

    msg, is_error, cleaned_data = trip_update_validate(data, trip)

    if is_error:
        return {
            "success": False,
            "error": "Validation error",
            "message": msg
        },400

    trip.destination = cleaned_data['destination']
    trip.start_date = cleaned_data['start_date']
    trip.end_date = cleaned_data['end_date']
    trip.budget = cleaned_data['budget']
    trip.max_travelers = cleaned_data['max_travelers']

    db.session.commit()

    return {
        "success": True,
        "message": "Trip updated successfully",
        "data": {
            "id": trip.id,
            "destination": trip.destination,
            "start_date": trip.start_date.isoformat(),
            "end_date": trip.end_date.isoformat(),
            "budget": trip.budget,
            "max_travelers": trip.max_travelers,
            "status": trip.status
        }
    }, 200

def update_trip_status(trip_id, data):
    trip = Trip.query.get(trip_id)

    if not trip:
        return {
            "success": False,
            "error": "Resource not found",
            "message": f"Trip with ID {trip_id} does not exist",
        },404

    msg, is_error, cleaned_data = trip_status_update_validate(data, trip)

    if is_error:
        return {
            "success": False,
            "error": "Validation error",
            "message": msg
        },400

    trip.status = cleaned_data['status']

    db.session.commit()

    return {
        "success": True,
        "message": "Trip status updated successfully",
        "data": {
            "id": trip.id,
            "destination": trip.destination,
            "start_date": trip.start_date.isoformat(),
            "end_date": trip.end_date.isoformat(),
            "budget": trip.budget,
            "max_travelers": trip.max_travelers,
            "status": trip.status
        }
    }, 200

def delete_trip(trip_id):
    trip = Trip.query.get(trip_id)

    if not trip:
        return {
            "success": False,
            "error": "Resource not found",
            "message": f"Trip with ID {trip_id} does not exist",
            "Data": None
        },404
    
    db.session.delete(trip)
    db.session.commit()

    return {
        "success": True,
        "message": "Trip deleted successfully"
    },200

def get_trip_summary(trip_id):
    trip = Trip.query.get(trip_id)

    if not trip:
        return {
            "success": False,
            "error": "Resource not found",
            "message": f"Trip with ID {trip_id} does not exist",
        },404

    total_expense = sum(expense.amount for expense in trip.expenses)
    remaining_budget = trip.budget - total_expense
    travelers = [{"id": traveler.id, "name": traveler.name, "email": traveler.email} for traveler in trip.travelers]
    expenses = [{"id": expense.id, "title": expense.title, "amount": expense.amount, "description": expense.description} for expense in trip.expenses]

    return {
        "success": True,
        "data": {
            "id": trip.id,
            "destination": trip.destination,
            "start_date": trip.start_date.isoformat(),
            "end_date": trip.end_date.isoformat(),
            "budget": trip.budget,
            "max_travelers": trip.max_travelers,
            "available_seats": trip.max_travelers - len(travelers),
            "status": trip.status,
            "travelers":{
                "traveler_count": len(travelers),
                "items": travelers
            },
            "expenses": {
                "total": total_expense,
                "remaining_budget": remaining_budget,
                "items": expenses
            },
        }
    }, 200


# Traveler service part---------------------------------------------------

def add_traveler_to_trip(trip_id, data):
    current_trip = Trip.query.get(trip_id)

    if not current_trip:
        return {
            "success": False,
            "error": "Resource not found",
            "message": f"Trip with ID {trip_id} does not exist",
        },404

    if current_trip.status != 'PLANNED':
        return {
            "success": False,
            "error": "Invalid operation",
            "message": "Travelers can only be added to PLANNED trips"
        },400

    msg, is_error, cleaned_data = traveler_create_validate(data)

    if is_error:
        return{
            "success": False,
            "error": "Validation error",
            "message": msg
        }, 400
    
    traveler = Traveler.query.filter_by(
        email = cleaned_data['email']
    ).first()

    if not traveler:
        traveler = Traveler(
            name=cleaned_data['name'],
            email=cleaned_data['email']
        )
        db.session.add(traveler)
    
    if traveler in current_trip.travelers:
        return {
            "success": False,
            "error": "Conflict",
            "message": f"Traveler is already added to {current_trip}"
        }, 409
    
    if len(current_trip.travelers) >= current_trip.max_travelers:
        return {
            "success": False,
            "error": "Trip_Full",
            "message": f"{current_trip} has reached the maximum number of travelers"
        }, 409

    overlapping_trip = Trip.query.filter(Trip.id != trip_id, Trip.status.in_(['PLANNED', 'ONGOING']),
                                        Trip.travelers.any(Traveler.id == traveler.id),
                                        Trip.start_date < current_trip.end_date,
                                        Trip.end_date > current_trip.start_date).first()

    if overlapping_trip:
        return {
            "success": False,
            "error": "Conflict",
            "message": f"Traveler already has an overlapping trip: {overlapping_trip}"
        },409

    current_trip.travelers.append(traveler)
    db.session.commit()
    return {"success": True,
            "message": f"Traveler added to {current_trip} successfully",
            "data": {
                "name": traveler.name,
                "email": traveler.email,
                "id": traveler.id
            }
        },201

def delete_traveler_from_trip(trip_id, traveler_id):
    current_trip = Trip.query.get(trip_id)

    if not current_trip:
        return {
            "success": False,
            "error": "Resource not found",
            "message": f"Trip with ID {trip_id} does not exist",
        },404
    
    traveler = Traveler.query.get(traveler_id)

    if not traveler:
        return {
            "success": False,
            "error": "Resource not found",
            "message": f"Traveler with ID {traveler_id} does not exist",
        },404

    if traveler not in current_trip.travelers:
        return {
            "success": False,
            "error": "Resource not found",
            "message": f"Traveler is not in this {current_trip}",
        },404

    if current_trip.status != 'PLANNED':
        return{
            "success": False,
            "error": "Traveler can't be removed",
            "message": "Travelers can only be removed from PLANNED trips"
        },400

    current_trip.travelers.remove(traveler)
    db.session.commit()

    return {
        "success": True,
        "message": f"Traveler removed from {current_trip} successfully",
        "Data": None
    },200


# Expense Service Part ------------------------------------------------

def add_expense_to_trip(trip_id, data):
    current_trip = Trip.query.get(trip_id)
    if not current_trip:
        return {
            "success": False,
            "error": "Resource not found",
            "message": f"Trip with ID {trip_id} does not exist",
        },404
    
    msg, is_error, cleaned_data = expense_create_validate(data)
    if is_error:
        return {
            "success": False,
            "error": "Validation error",
            "message": msg
        },400
    


    if current_trip.status not in ['PLANNED', 'ONGOING']:
        return {
            "success": False,
            "error": "Invalid operation",
            "message": "Expenses can only be added to PLANNED or ONGOING trips"
        },400

    total_expense = 0
    for expense in current_trip.expenses:
        total_expense += expense.amount
    
    if total_expense + cleaned_data['amount'] > current_trip.budget:
        return{
            "success": False,
            "error" : "Invalid operation",
            "message": f"Adding this expense would exceed the {current_trip} budget"
        }, 400

    expense = Expense(
        title=cleaned_data['title'],
        amount=cleaned_data['amount'],
        description=cleaned_data['description']
    )
    db.session.add(expense)
    
    current_trip.expenses.append(expense)
    db.session.commit()

    return {
        "success": True,
        "message": f"Expense added to {current_trip} successfully",
        "data": {
            "id": expense.id,
            "title": expense.title,
            "amount": expense.amount,
            "description": expense.description
        }
    },201