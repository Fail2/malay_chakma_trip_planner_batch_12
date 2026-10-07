def expense_create_validate(data):
    required_fields = [
        'title',
        'amount',
        'description'
    ]

    # Request Validation
    if not isinstance(data, dict):
        return "Request body must be a JSON object", True, None
    
    # Field validation
    for field in required_fields:
        if field not in data:
            return f"{field} is required", True, None
    
    # Expense title validation
    if not isinstance(data['title'],str):
        return "Title must be a string", True, None
    title = data['title'].strip()
    if not title:
        return "Title field can't be empty", True, None
    if len(title)>50:
        return "Title length can't exceed 50", True, None

    # Expense amount validation
    if isinstance(data['amount'],bool) or not isinstance(data['amount'],(int, float)):
        return "Amount must be a number", True, None
    amount = data['amount']
    if amount <= 0:
        return "Amount must be greater than 0", True, None

    # Expense description validation
    if not isinstance(data['description'],str):
        return "Description must be a string", True, None
    description = data['description'].strip()
    if not description:
        return "Description field can't be empty", True, None
    if len(description)>200:
        return "Description length can't exceed 200", True, None

    # Cleaned Data
    cleaned_data = {
        "title":title,
        "amount":amount,
        "description":description
    }

    return "", False, cleaned_data
    
