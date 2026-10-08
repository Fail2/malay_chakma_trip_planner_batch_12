from flask import Blueprint, request

trips_bp = Blueprint('trips',__name__)


# Manage Trip Part------------------------------------

@trips_bp.get('/')
def list_trips_route():
    response, status_code = list_trips()

    return response, status_code
@trips_bp.get('/<int:trip_id>')
def get_trip_route(trip_id):
    response, status_code = get_trip(trip_id)

    return response, status_code

@trips_bp.post('/')
def create_trip_route():
    data = request.get_json()
    response, status_code = create_trip(data)

    return response, status_code


@trips_bp.put('/<int:trip_id>')
def update_trip_route(trip_id):
    data = request.get_json()
    response, status_code = update_trip(trip_id, data)

    return response, status_code

@trips_bp.delete('/<int:trip_id>')
def delete_trip_route(trip_id):
    response, status_code = delete_trip(trip_id)

    return response, status_code



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

# Manage Expense Part------------------------------------------

@trips_bp.post('/<int:trip_id>/expense')
def add_expense_to_trip_route(trip_id):
    data = request.get_json()

    response, status_code = add_expense_to_trip(trip_id, data)

    return response, status_code
