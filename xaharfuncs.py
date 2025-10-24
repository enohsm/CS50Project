from datetime import datetime
from re import match
from flask import redirect, session, flash, url_for
from functools import wraps
import requests

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
    

def valid_name(name):
    if not name.replace(" ", "").isalpha():
        return False
    return True


def valid_location(province, district):
    api_url = "https://api.turkiyeapi.dev/v1/provinces"

    response = requests.get(api_url)
    if response.status_code != 200:
        return False
    
    data = response.json().get("data", [])

    provinces = [p["name"] for p in data]
    if province not in provinces:
        return False
    
    p_data = next((p for p in data if p["name"] == province), None)

    districts = [d["name"] for d in p_data["districts"]]

    return district in districts


def valid_plate(plate):
    pattern = r"^[0-9]{2}[A-Za-z]{1,3}[0-9]{1,4}$"

    return bool(match(pattern, plate))


def valid_vin(vin):
    pattern = r"^[0-9A-Za-z]{17}$"

    return bool(match(pattern, vin))


def valid_brand(brand):
    pattern = r"^[A-Za-z -\.]+$"

    return bool(match(pattern, brand))


def valid_type(type):
    pattern = r"^[A-Za-z0-9\,\. -]+$"

    return bool(match(pattern, type))


def valid_color(color):
    pattern = r"^[A-Za-z\(\) ]+$"

    return bool(match(pattern, color))
