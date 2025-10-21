from datetime import datetime
from re import match
from flask import redirect, session, flash, url_for
from functools import wraps

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

def login_required(arg=None):
    if callable(arg):
        func = arg

        @wraps(func)
        
        def xahar_login(*args, **kwargs):
            if "user_id" not in session:
                flash("Please login to see this page.")
                return redirect(url_for("main.login"))
            return func(*args, **kwargs)
        
        return xahar_login
    
    else:
        role = arg

        def login_required_permission(func):
            @wraps(func)

            def xahar_login(*args, **kwargs):
                if "user_id" not in session:
                    flash("Please login to see this page.")
                    return redirect(url_for("main.login"))
                
                else:
                    if session["role"] != role:
                        flash("You do not have permission to see this page.")
                        return redirect(url_for("main.homepage"))
                    return func(*args, **kwargs)
            
            return xahar_login
        return login_required_permission