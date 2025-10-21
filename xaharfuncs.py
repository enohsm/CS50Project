from datetime import datetime
from re import match

# EN: 
# TR: Programımda kullandığım kendi fonksiyonlarım

def match_passwords(password, confirmation):
    if password == confirmation:
        return True
    else:
        return False
    
def valid_date(birth):
    try:
        return datetime.strptime(birth, "%Y-%m-%d").strftime("%d/%m/%Y")
    except ValueError:
        return False
    
def valid_password(password):
    pattern = "^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])(?=.{8,}).*$"
    if bool(match(pattern, password)) and len(password) >= 8:
        return True
    else:
        return False

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
    pattern = r"^[a-z0-9]+([._-][a-z0-9]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*\.[a-z]{2,}$"
    if match(pattern, email):
        return True
    else:
        return False
    
def valid_contact(contact):
    if contact.isdigit() and len(contact) == 11:
        return True
    else:
        return False

def isexisting(table, key, value):
    from routes.imports import DataBase
    isexist = DataBase.execute(f"SELECT * FROM {table} WHERE {key} = ?", value)
    return bool(isexist)