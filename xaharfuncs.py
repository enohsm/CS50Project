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
    if not bool(match(pattern, password)):
        return False
    if not len(password) >= 8:
        return False
    return True

def valid_namesurname(name, surname):
    if name.isalpha() and surname.isalpha():
        return True
    else:
        return False

def valid_identification(ident_no):
    if ident_no.isdigit() and len(ident_no) == 11:
        return True
    else:
        return False
    
def valid_email(email):
    if email:
        return True
    else:
        return False
    
def valid_contact(contact):
    if:
        return True
    else:
        return False