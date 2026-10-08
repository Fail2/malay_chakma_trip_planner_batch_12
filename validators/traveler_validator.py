import re

def traveler_create_validate(data):
    required_fields = [
        'name',
        'email'
    ]

    # Request Validation
    if not isinstance(data, dict):
        return "Request body must be a JSON object", True, None
    
    # Field validation
    for field in required_fields:
        if field not in data:
            return f"{field} is required", True, None
    
    # Name validation
    if not isinstance(data['name'],str):
        return "Name must be a string", True, None
    name = data['name'].strip()
    if not name:
        return "Name field can't be empty", True, None
    if len(name)>100:
        return "Name length can't exceed 100", True, None

    name_pattern = r'^[A-Za-z0-9 ]+$'
    if not re.fullmatch(name_pattern, name):
        return "Invalid name format - name can contain only letters, numbers and spaces", True, None

    
    # Email validation
    if not isinstance(data['email'],str):
        return "Email must be a string", True, None
    email = data['email'].strip().lower()
    if not email:
        return "Email field can't be empty", True, None
    if len(email)>120:
        return "Email length can't exceed 120", True, None
    

    email_pattern = r'^[A-Za-z0-9]+(?:[._-][A-Za-z0-9]+)*@[A-Za-z0-9]+(?:[.-][A-Za-z0-9]+)*\.[A-Za-z]{2,}$'
    if not re.fullmatch(email_pattern, email):
        return "Invalid email format", True, None
    
    
    # Cleaned Data
    cleaned_data = {
        "name":name,
        "email":email,
    }

    return "", False, cleaned_data
    
