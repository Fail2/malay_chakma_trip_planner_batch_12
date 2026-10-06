from flask import Blueprint, jsonify, render_template
from app.models import Trip

trips_bp = Blueprint('trips',__name__)

@trips_bp.route('/', methods=['GET'])
def list_trips():
    trips = Trip.query.all()
    return jsonify([{"destination": trip.destination, "start_date": trip.start_date, "end_date": trip.end_date, "budget": trip.budget, "max_travelers": trip.max_travelers, "status": trip.status} for trip in trips])

@trips_bp.route('/<int:trip_id>', methods=['GET'])
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