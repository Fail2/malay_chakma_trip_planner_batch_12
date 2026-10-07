from app.models import Trip, Traveler, Expense
from app import db
from validators.traveler_validator import traveler_create_validate
from validators.expense_validator import expense_create_validate

def add_traveler_to_trip(trip_id, data):
    current_trip = Trip.query.get(trip_id)

    if not current_trip:
        return {
            "success": False,
            "error": "Trip not found",
            "message": f"Trip with ID {trip_id} does not exist",
        },404

    if current_trip.status != 'planned':
        return {
            "success": False,
            "error": "Traveler cannot be added",
            "message": "Travelers can only be added to planned trips"
        },400

    msg, is_error, cleaned_data = traveler_create_validate(data)

    if is_error:
        return{
            "success": False,
            "error": "Traveler details invalid",
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
            "error": "Traveler already exists in this trip",
            "message": f"Traveler is already added to {current_trip}"
        }, 400
    
    if len(current_trip.travelers) >= current_trip.max_travelers:
        return {
            "success": False,
            "error": "Trip is full",
            "message": f"{current_trip} has reached the maximum number of travelers"
        }, 400

    overlapping_trip = Trip.query.filter(Trip.id != trip_id, Trip.travelers.any(Traveler.id == traveler.id),
                                          Trip.start_date < current_trip.end_date,
                                          Trip.end_date > current_trip.start_date ).first()

    if overlapping_trip:
        return {
            "success": False,
            "error": "Traveler has another overlapping trip",
            "message": f"Traveler already has an overlapping trip: {overlapping_trip}"
        },400

    current_trip.travelers.append(traveler)
    db.session.commit()
    return {"success": True,
            "message": f"Traveler added to {current_trip} successfully",
            "data": {
                "name": traveler.name,
                "email": traveler.email,
                "id": traveler.id
            }
        },200

def delete_traveler_from_trip(trip_id, traveler_id):
    current_trip = Trip.query.get(trip_id)

    if not current_trip:
        return {
            "success": False,
            "error": "Trip not found",
            "message": f"Trip with ID {trip_id} does not exist",
        },404
    
    traveler = Traveler.query.get(traveler_id)

    if not traveler:
        return {
            "success": False,
            "error": "Traveler not found",
            "message": f"Traveler with ID {traveler_id} does not exist",
        },404

    if traveler not in current_trip.travelers:
        return {
            "success": False,
            "error": "Traveler is not in this trip",
            "message": f"Traveler is not in this {current_trip}",
        },404

    if current_trip.status != 'planned':
        return{
            "success": False,
            "error": "Traveler can't be removed",
            "message": "Travelers can only be removed from planned trips"
        },400

    current_trip.travelers.remove(traveler)
    db.session.commit()

    return {
        "success": True,
        "message": f"Traveler removed from {current_trip} successfully"
    },200

def add_expense_to_trip(trip_id, data):
    msg, is_error, cleaned_data = expense_create_validate(data)
    if is_error:
        return {
            "success": False,
            "error": "Request Data is not valid",
            "message": msg
        },400
    
    current_trip = Trip.query.get(trip_id)
    if not current_trip:
        return {
            "success": False,
            "error": "Trip not found",
            "message": f"Trip with ID {trip_id} does not exist",
        },404

    if current_trip.status not in ['planned', 'ongoing']:
        return {
            "success": False,
            "error": "Expense cannot be added",
            "message": "Expenses can only be added to planned or ongoing trips"
        },400

    total_expense = 0
    for expense in current_trip.expenses:
        total_expense += expense.amount
    
    if total_expense + cleaned_data['amount'] > current_trip.budget:
        return{
            "success": False,
            "error" : "Expense can't be added",
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
        "message": f"Expense added to {current_trip} successfully"
    },200