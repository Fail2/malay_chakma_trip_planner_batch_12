from datetime import datetime

def trip_validate(data):
    required_fields = [
        'destination',
        'start_date',
        'end_date',
        'budget',
        'max_travelers'
    ]

    for field in required_fields:
        if field not in data:
            return f"{field} is required", True, None
    
    if not isinstance(data['destination'],str):
        return "Destination must be a string", True, None
    destination = data['destination'].strip()
    if not destination:
        return "Destination field can't be empty", True, None
    if len(destination)>100:
        return "Destination length can't exceed 100", True, None
    
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
    if start_date >= end_date:
        return "Trip must be at least 1 day", True, None

    if not isinstance(data['budget'],(int, float)):
        return "Budget must be a number", True, None
    budget = data['budget']
    if budget <= 0:
        return "Budget must be greater than 0", True, None

    if not isinstance(data['max_travelers'],int):
        return "Max travelers must be an integer", True, None
    max_travelers = data['max_travelers']
    if max_travelers < 1:
        return "Max travelers at least 1", True, None

    cleaned_data = {
        "destination": destination,
        "start_date": start_date,
        "end_date": end_date,
        "budget": budget,
        "max_travelers": max_travelers
    }

    return "", False, cleaned_data

def trip_update_validate(data, current_status):
    required_fields = [
        'destination',
        'start_date',
        'end_date',
        'budget',
        'max_travelers',
        'status'
    ]

    for field in required_fields:
        if field not in data:
            return f"{field} is required", True, None
    
    if not isinstance(data['destination'],str):
        return "Destination must be a string", True, None
    destination = data['destination'].strip()
    if not destination:
        return "Destination field can't be empty", True, None
    if len(destination)>100:
        return "Destination length can't exceed 100", True, None
    
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
    if start_date >= end_date:
        return "Trip must be at least 1 day", True, None

    if not isinstance(data['budget'],(int, float)):
        return "Budget must be a number", True, None
    budget = data['budget']
    if budget <= 0:
        return "Budget must be greater than 0", True, None

    if not isinstance(data['max_travelers'],int):
        return "Max travelers must be an integer", True, None
    max_travelers = data['max_travelers']
    if max_travelers < 1:
        return "Max travelers at least 1", True, None

    if not isinstance(data['status'],str):
        return "Status must be a string", True, None
    status = data['status'].strip()
    if not status:
        return "Status field can't be empty", True, None
    if status not in ['planned', 'ongoing', 'completed', 'cancelled']:
        return "Choose a valid status", True, None
    
    if current_status == 'planned':
        if status not in ['cancelled', 'ongoing']:
            return "Planned trip can only transform to ongoing or cancelled", True, None
    if current_status == 'ongoing':
        if status not in ['cancelled', 'completed']:
            return "Ongoing trip can only transform to completed or cancelled", True, None
    if current_status in ['cancelled', 'completed']:
        return "Can't change the status of cancelled or completed trips", True, None

    cleaned_data = {
        "destination": destination,
        "start_date": start_date,
        "end_date": end_date,
        "budget": budget,
        "max_travelers": max_travelers,
        'status': status
    }

    return "", False, cleaned_data
