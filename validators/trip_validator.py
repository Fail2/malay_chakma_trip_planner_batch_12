from datetime import datetime, date
from math import isfinite
from app.models import Trip

def trip_create_validate(data):
    required_fields = [
        'destination',
        'start_date',
        'end_date',
        'budget',
        'max_travelers'
    ]
    # Request validation
    if not isinstance(data, dict):
        return "Request body must be a JSON object", True, None

    # Fields validation
    for field in required_fields:
        if field not in data:
            return f"{field} is required", True, None
    
    # Destination validation
    if not isinstance(data['destination'],str):
        return "Destination must be a string", True, None
    destination = data['destination'].strip()
    if not destination:
        return "Destination field can't be empty", True, None
    if len(destination)>100:
        return "Destination length can't exceed 100", True, None
    
    # Dates validation
    if not isinstance(data['start_date'], str):
        return "Start date must be a string", True, None
    if not isinstance(data['end_date'], str):
        return "End date must be a string", True, None

    start_date = data['start_date'].strip()
    if not start_date:
        return "Start date field can't be empty", True, None
    end_date = data['end_date'].strip()
    if not end_date:
        return "End date field can't be empty", True, None
    try:
        start_date = datetime.strptime(start_date,"%Y-%m-%d").date()
        end_date = datetime.strptime(end_date,"%Y-%m-%d").date()
    except ValueError:
        return "Date must be in YYYY-MM-DD format", True, None
    
    today = date.today()
    if start_date < today or end_date < today:
        return "Trip start or end date must be current or upcoming date", True, None
    if start_date >= end_date:
        return "End date must be after start date", True, None

    # Budget validation
    if isinstance(data['budget'],bool) or not isinstance(data['budget'],(int, float)) or not isfinite(data['budget']):
        return "Budget must be a number", True, None
    budget = data['budget']
    if budget <= 0:
        return "Budget must be greater than 0", True, None

    # Max travelers validation
    if isinstance(data['max_travelers'], bool) or not isinstance(data['max_travelers'],int) or not isfinite(data['max_travelers']):
        return "Max travelers must be an integer", True, None
    max_travelers = data['max_travelers']
    if max_travelers < 1:
        return "Max travelers at least 1", True, None

    # Cleaned data
    cleaned_data = {
        "destination": destination,
        "start_date": start_date,
        "end_date": end_date,
        "budget": budget,
        "max_travelers": max_travelers
    }

    return "", False, cleaned_data

def trip_update_validate(data, current_trip):
    required_fields = [
        'destination',
        'start_date',
        'end_date',
        'budget',
        'max_travelers'
    ]
    # Request validation
    if not isinstance(data, dict):
        return "Request body must be a JSON object", True, None
   
    # Cancelled or Completed trips validation
    if current_trip.status in ['CANCELLED', 'COMPLETED']:
        return "You can't change anything for CANCELLED or COMPLETED Trip", True, None
    
    # Trip fields validation
    for field in required_fields:
        if field not in data:
            return f"{field} is required", True, None
    
    # Trip destination validation
    if not isinstance(data['destination'],str):
        return "Destination must be a string", True, None
    destination = data['destination'].strip()
    if not destination:
        return "Destination field can't be empty", True, None
    if len(destination)>100:
        return "Destination length can't exceed 100", True, None
    
    # Trip dates validation
    if not isinstance(data['start_date'], str):
        return "Start date must be a string", True, None
    if not isinstance(data['end_date'], str):
        return "End date must be a string", True, None

    start_date = data['start_date'].strip()
    if not start_date:
        return "Start date field can't be empty", True, None
    end_date = data['end_date'].strip()
    if not end_date:
        return "End date field can't be empty", True, None
    try:
        start_date = datetime.strptime(start_date,"%Y-%m-%d").date()
        end_date = datetime.strptime(end_date,"%Y-%m-%d").date()
    except ValueError:
        return "Date must be in YYYY-MM-DD format", True, None
    today = date.today()
    if start_date < today or end_date < today:
        return "Trip start or end date must be current or upcoming date", True, None
    if start_date >= end_date:
        return "End date must be after start date", True, None

    # Trip budget validation
    if isinstance(data['budget'],bool) or not isinstance(data['budget'],(int, float)) or not isfinite(data['budget']):
        return "Budget must be a number", True, None
    budget = data['budget']
    if budget <= 0:
        return "Budget must be greater than 0", True, None

    # Trip max travelers validation
    if isinstance(data['max_travelers'], bool) or not isinstance(data['max_travelers'],int) or not isfinite(data['max_travelers']):
        return "Max travelers must be an integer", True, None
    max_travelers = data['max_travelers']
    if max_travelers <= 0:
        return "Max travelers must be greater than 0", True, None
    
    
    # Ongoing trip validation
    if current_trip.status == 'ONGOING':
        if destination != current_trip.destination:
            return "Can't change ONGOING trip destination", True, None
        if start_date != current_trip.start_date:
            return "Can't change ONGOING trip start date", True, None
        if end_date != current_trip.end_date:
            return "Can't change ONGOING trip end date", True, None
        if budget != current_trip.budget:
            return "Can't change ONGOING trip budget", True, None
        if max_travelers != current_trip.max_travelers:
            return "Can't change ONGOING trip max travelers", True, None

    # Cleaned data
    cleaned_data = {
        "destination": destination,
        "start_date": start_date,
        "end_date": end_date,
        "budget": budget,
        "max_travelers": max_travelers,
    }

    return "", False, cleaned_data

def trip_status_update_validate(data, current_trip):
    # Request validation
    if not isinstance(data, dict):
        return "Request body must be a JSON object", True, None
       
    # Cancelled or Completed trips validation
    if current_trip.status in ['CANCELLED', 'COMPLETED']:
        return "You can't change anything for CANCELLED or COMPLETED Trip", True, None
        
    # Trip status check 
    if 'status' not in data:
        return "status is required", True, None

    # Trip status validation
    if not isinstance(data['status'],str):
        return "Status must be a string", True, None
    status = data['status'].strip().upper()
    if not status:
        return "Status field can't be empty", True, None
    if status not in ['PLANNED', 'ONGOING', 'COMPLETED', 'CANCELLED']:
        return "Choose a valid status", True, None

    if current_trip.status == 'PLANNED':
        if status not in ['CANCELLED', 'ONGOING']:
            return "Planned trip can only transform to ONGOING or CANCELLED", True, None
    if current_trip.status == 'ONGOING':
        if status not in ['COMPLETED', 'CANCELLED']:
            return "Ongoing trip can only transform to COMPLETED or CANCELLED", True, None
    
    cleaned_data = {
        "status": status
    }   

    return "", False, cleaned_data

def get_total_expense(expenses):
    total = 0
    for expense in expenses:
        total+= expense.amount
    return total