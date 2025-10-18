from datetime import datetime
from re import match

# EN: 
# TR: Programımda kullandığım kendi fonksiyonlarım

# EN:
# TR: Parola eşleşmesi
def match_passwords(password, confirmation):
    if password == confirmation:
        return True
    else:
        return False
    
def valid_date(birth):
    try:
        datetime.strptime(birth, "%d/%m/%Y")
        return True
    except ValueError:
        return False
    
def valid_password(password):
    pattern = "^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])(?=.{8,}).*$"
    return bool(match(pattern, password))