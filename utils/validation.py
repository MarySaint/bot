import re

def validate_phone_number(phone_number):
    pattern = r'^8\d{3}\d{3}\d{2}\d{2}$'
    if re.fullmatch(pattern, phone_number):
        return True
    else:
        return False