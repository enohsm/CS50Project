from datetime import datetime, timedelta
from re import match
from flask import redirect, session, flash, url_for
from functools import wraps
import requests
from werkzeug.utils import secure_filename
from uuid import uuid4

# EN: My custom functions used in this program
# TR: Programımda kullandığım kendi fonksiyonlarım

def match_passwords(password, confirmation):
    '''This function performs password matching.'''
    if password == confirmation:
        return True
    else:
        return False
    

def valid_date(date):
    '''This function checks whether a date format is valid; if it is invalid, it returns False, and if it is valid, it returns the date as a string in the format DD/MM/YYYY.'''
    try:
        return datetime.strptime(date, "%Y-%m-%d").strftime("%d/%m/%Y")
    except ValueError:
        return False
    

def valid_birthdate(birth):
    '''This function checks the validity of a birth date and returns a boolean value.'''
    try:
        if not datetime.strptime(birth, '%Y-%m-%d') < datetime.today():
            return False
        return True
    except ValueError:
        return False


def valid_expdate(expdate):
    '''This function checks whether the passport’s validity date is at least one year later and returns a boolean value.'''
    try:
        if not datetime.strptime(expdate, '%Y-%m-%d') > (datetime.today() + timedelta(days = 364)):
            return False
        return True
    except:
        return False
    
    
def valid_password(password):
    '''It checks whether the password is valid. Does the pattern match? Is it at least 8 characters long?'''
    pattern = "^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])(?=.{8,}).*$"
    if bool(match(pattern, password)) and len(password) >= 8:
        return True
    else:
        return False
   

def valid_namesurname(name, surname):
    '''It performs a name–surname check and verifies whether it consists of alphabetic characters.'''
    if name.isalpha() and surname.isalpha():
        return True
    else:
        return False
    

def valid_identification(ident_no):
    '''It checks the identity number.'''
    if ident_no.isdigit() and len(ident_no) == 11:
        return True
    else:
        return False
    
    
def valid_email(email):
    '''It checks the pattern of the email address.'''
    pattern = r"^[a-z0-9]+([._-][a-z0-9]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*\.[a-z]{2,}$"
    if match(pattern, email):
        return True
    else:
        return False
    

def valid_contact(contact):
    '''It checks whether the phone number consists of 11 digits.'''
    if contact.isdigit() and len(contact) == 11:
        return True
    else:
        return False


def isexisting(table, key, value):
    '''This function checks whether rows exist for a value in a table.'''
    from routes.imports import DataBase
    isexist = DataBase.execute(f"SELECT * FROM {table} WHERE {key} = ?", value)
    return bool(isexist)


def login_required(arg=None):
    '''This function checks the session for route access and also verifies whether the user has permission for routes that require authorization.'''
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
        str_role = arg
        role = 0

        if str_role == 'employee':
            role = 1
        
        elif str_role == 'admin':
            role = 2

        def login_required_permission(func):
            @wraps(func)

            def xahar_login(*args, **kwargs):
                if "user_id" not in session:
                    flash("Please login to see this page.")
                    return redirect(url_for("main.login"))
                
                else:
                    if session["role"] < role:
                        flash("You do not have permission to see this page.")
                        return redirect(url_for("main.homepage"))
                    return func(*args, **kwargs)
            
            return xahar_login
        return login_required_permission
    

def valid_name(name):
    '''It checks whether the name consists of alphabetic characters.'''
    if not name.replace(" ", "").isalpha():
        return False
    return True


def valid_location(province, district):
    '''It checks the validity of a location via an API.'''
    api_url = "https://api.turkiyeapi.dev/v1/provinces"

    response = requests.get(api_url)
    if response.status_code != 200:
        return False
    
    data = response.json().get("data", [])
    if not data:
        return False

    provinces = [p["name"] for p in data]
    if province not in provinces:
        return False
    
    p_data = next((p for p in data if p["name"] == province), None)

    districts = [d["name"] for d in p_data["districts"]]

    return district in districts


def valid_plate(plate):
    '''It checks the validity of a vehicle license plate using a pattern.'''
    pattern = r"^[0-9]{2}[A-Za-z]{1,3}[0-9]{1,4}$"

    return bool(match(pattern, plate))


def valid_vin(vin):
    '''It checks the validity of a vehicle chassis number using a pattern.'''
    pattern = r"^[0-9A-Za-z]{17}$"

    return bool(match(pattern, vin))


def valid_brand(brand):
    '''It checks the vehicle brand using a pattern.'''
    pattern = r"^[A-Za-z -.]+$"

    return bool(match(pattern, brand))


def valid_type(type_):
    '''It checks the vehicle type using a pattern.'''
    pattern = r"^[A-Za-z0-9,.\- ]+$"

    return bool(match(pattern, type_))


def valid_color(color):
    '''It checks the allowed characters when entering the vehicle color using a pattern.'''
    pattern = r"^[A-Za-z\(\) ]+$"

    return bool(match(pattern, color))


def valid_passno(pass_no):
    '''It checks whether the passport number is in the correct format.'''
    pattern = r"^[A-Za-z]?[0-9]{8}$"
    
    return bool(match(pattern, pass_no))


def apology(message, route, **values):
    '''It returns a message to the user and performs a redirect. Usage: apology('Success!', 'main.homepage')'''
    flash(message)
    return redirect(url_for(route, **values))


def valid_country(country):
    '''It checks whether the country to be applied for is among the available application countries.'''
    countries = ['BULGARIA', 'GREECE', 'GERMANY', 'NETHERLANDS', 'AUSTRIA', 'ITALY']

    if country not in countries:
        return False
    
    return True


def valid_prefdate(pref_date):
    '''It checks whether the chosen date is at least two weeks later.'''
    if datetime.strptime(pref_date, '%Y-%m-%d') < (datetime.today() + timedelta(weeks = 2)):
        return False
    return True


def visatype(birth):
    '''It determines the visa type based on the date of birth.'''
    visatype = ''

    if (datetime.today() - datetime.strptime(birth, '%d/%m/%Y')) >= timedelta(days = 365 * 12):
        visatype = 'With Biometric'
    
    else:
        visatype = 'Without Biometric'

    return visatype


def file_query(file):
    '''It executes a query using an SQL file. Usage: file_query('query.sql')'''
    with open(f'queries/{file}', 'r') as readf:
        return readf.read()


def countries():
    '''It returns the list of countries.'''
    return ['BULGARIA', 'GREECE', 'GERMANY', 'NETHERLANDS', 'AUSTRIA', 'ITALY']


def valid_startdate(start_date):
    '''It checks whether the insurance start date is at least today.'''
    try:
        startdate = datetime.strptime(start_date, '%Y-%m-%d')
        if startdate.date() < datetime.today().date():
            return False
        return True
    except ValueError:
        return False
    

def valid_image(image):
    '''It reads an image file and checks the metadata to verify whether it is an actual image file.'''
    meta = image.read(8)
    image.seek(0)
    print(meta)
    if meta == b'\x89PNG\r\n\x1a\n' or meta[:3] == b'\xff\xd8\xff':
        return True
    
    else:
        return False
    

def new_filename(filename):
    '''It generates a secure filename.'''
    sec_filename = secure_filename(filename.lower())
    ext = f'.{sec_filename.rsplit('.', 1)[-1]}'
    new_filename = f'{uuid4().hex}{ext}'
    
    return new_filename