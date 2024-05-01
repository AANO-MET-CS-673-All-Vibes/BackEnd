from datetime import datetime

# Input validation function for gender
def validate_gender(gender):
    if gender not in [0, 1]:  # Assuming 0 is male, 1 is female
        return False
    return True


# Input validation function for date of birth (dob)
def validate_dob(dob):
    try:
        datetime.strptime(dob, '%Y-%m-%d')
        return True
    except ValueError:
        return False

# Validation for name
def validate_name(name):
    if name is None or not isinstance(name, str) or len(name) < 2 or len(name) > 30:
        return False
    return True

# Input validation function for biography (bio)
def validate_bio(bio):
    if bio is None or not isinstance(bio, str) or len(bio) > 300: # 300 max length can be changed
        return False
    return True

