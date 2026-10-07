from flask import Blueprint, jsonify, render_template, request
from app.models import Trip, Traveler
from validators.trip_validator import trip_create_validate, trip_update_validate
from validators.traveler_validator import traveler_create_validate
from app.services import add_traveler_to_trip, delete_traveler_from_trip
from app import db


trips_bp = Blueprint('trips',__name__)

@trips_bp.get('/')
def list_trips():
    trips = Trip.query.all()
    return jsonify([{"id": trip.id, "destination": trip.destination, "start_date": trip.start_date, "end_date": trip.end_date, "budget": trip.budget, "max_travelers": trip.max_travelers, "status": trip.status} for trip in trips])

@trips_bp.get('/<int:trip_id>')
def get_list(trip_id):
    trip = Trip.query.get(trip_id)

    if not trip:
        return {
            "success": False,
            "error": "Trip not found",
            "message": f"Trip with ID {trip_id} does not exitst",
        },404

    return {
        "success": True,
        "data": {"destination": trip.destination, "start_date": trip.start_date, 
        "end_date": trip.end_date, "budget": trip.budget, 
        "max_travelers": trip.max_travelers, "status": trip.status}
        }, 200

@trips_bp.post('/')
def create_trip():
    data = request.get_json()
    msg, is_error, cleaned_data = trip_create_validate(data)

    if is_error:
        return {
            "success": False,
            "error": msg
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


@trips_bp.put('/<int:trip_id>')
def trip_update(trip_id):
    trip = Trip.query.get(trip_id)

    if not trip:
        return {
            "success": False,
            "error": "Trip not found",
            "message": f"Trip with ID {trip_id} does not exitst",
        },404

    data = request.get_json()
    msg, is_error, cleaned_data = trip_update_validate(data, trip)

    if is_error:
        return {
            "success": False,
            "error": msg
        },400

    trip.destination = cleaned_data['destination']
    trip.start_date = cleaned_data['start_date']
    trip.end_date = cleaned_data['end_date']
    trip.budget = cleaned_data['budget']
    trip.max_travelers = cleaned_data['max_travelers']
    trip.status = cleaned_data['status']


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

@trips_bp.delete('/<int:trip_id>')
def trip_delete(trip_id):
    trip = Trip.query.get(trip_id)

    if not trip:
        return {
            "success": False,
            "error": "Trip not found",
            "message": f"Trip with ID {trip_id} does not exitst",
        },404
    
    db.session.delete(trip)
    db.session.commit()

    return {
        "success": True,
        "message": "Trip deleted successfully"
    },200

# Manage Traveler Part -----------------------------------------

@trips_bp.post('/<int:trip_id>/travelers')
def add_traveler_to_trip_route(trip_id):
    data = request.get_json()

    response, status_code = add_traveler_to_trip(trip_id, data)

    return response, status_code

@trips_bp.delete('/<int:trip_id>/travelers/<int:traveler_id>')
def delete_traveler_from_trip_route(trip_id, traveler_id):
    response, status_code = delete_traveler_from_trip(trip_id, traveler_id)

    return response, status_code