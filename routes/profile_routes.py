from .imports import *


# ENG: Assign a variable for the profile routes blueprint
# TR: Profil rotalarını modülleyecek bir değişken ata
profilebp = Blueprint("profile", __name__, url_prefix="/me")


# Profil route ayarla
@profilebp.route("/")
@x.login_required
def profile():
    return render_template("profile.html")


# Araçlar routeunu ayarla
@profilebp.route("/vehicles")
@x.login_required
def vehicles():
    vehicles = DataBase.execute("SELECT * FROM vehicles WHERE user_id = ?", session["user_id"])
    return render_template("my_vehicles.html", vehicles=vehicles)


@profilebp.route("/vehicles/add", methods=["GET", "POST"])
@x.login_required
def add_vehicle():
    if request.method == "POST":
        name = request.form.get("name")
        if not name or not x.valid_name(name):
            flash("Invalid name")
            return redirect(url_for("profile.add_vehicle"))
        
        province = request.form.get("province")
        district = request.form.get("district")
        if not province or not district or not x.valid_location(province, district):
            flash("Invalid location.")
            return redirect(url_for("profile.add_vehicle"))
        
        plate = request.form.get("plate")
        if not plate or not x.valid_plate(plate):
            flash("Invalid plate.")
            return redirect(url_for("profile.add_vehicle"))
        
        vin = request.form.get("vin")
        if not vin or not x.valid_vin(vin):
            flash("Invalid VIN.")
            return redirect(url_for("profile.add_vehicle"))
        
        brand = request.form.get("brand")
        if not brand or not x.valid_brand(brand):
            flash("Invalid brand.")
            return redirect(url_for("profile.add_vehicle"))
        
        type = request.form.get("type")
        if not type or not x.valid_type(type):
            flash("Invalid type.")
            return redirect(url_for("profile.add_vehicle"))
        
        color = request.form.get("color")
        if not color or not x.valid_color(color):
            flash("Invalid color.")
            return redirect(url_for("profile.add_vehicle"))

        vehicle_img = request.files.get('vehicle_img')
        if not vehicle_img:
            return x.apology('Invalid vehicle image.', 'profile.add_vehicle')

        if not x.valid_image(vehicle_img):
            return x.apology('Invalid vehicle image.', 'profile.add_vehicle')
    
        if not len(vehicle_img.filename.rsplit('.', 1)) > 1:
            return x.apology('Invalid vehicle image.', 'profile.add_vehicle')
        
        if vehicle_img.filename.lower().rsplit('.', 1)[-1] not in ['jpg', 'jpeg', 'png']:
            return x.apology('Invalid vehicle image.', 'profile.add_vehicle')

        vehicle = DataBase.execute("SELECT id FROM vehicles WHERE user_id = ? AND plate = ? OR vin = ?", session["user_id"], plate, vin)
        if vehicle:
            flash("This vehicle is already in your vehicle list.")
            return redirect(url_for("profile.add_vehicle"))
        
        try:
            filename = x.new_filename(vehicle_img.filename)
            DataBase.execute("INSERT INTO vehicles (user_id, namesurname, address, plate, vin, brand, model, color, img) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)", session["user_id"], name.upper(), (district.upper()+"/"+province.upper()), plate.upper(), vin.upper(), brand.upper(), type.upper(), color.upper(), filename)
            vehicle_img.save(os.path.join('static', 'vehicles', filename))
            flash("Your vehicle has successfully registered.")
            return redirect(url_for("profile.vehicles"))
        
        except ValueError:
            return x.apology('An error occurred. Please try again.', 'profile.add_vehicle')
        
    else:
        return render_template("add_vehicle.html")
    

@profilebp.route('/vehicles/view')
@x.login_required
def view_vehicle():
    vehicle_id = request.args.get('id')
    if not vehicle_id or not vehicle_id.isdigit():
        return redirect('profile.vehicles')
    
    is_users_vehicle = DataBase.execute('SELECT * FROM vehicles WHERE id = ? AND user_id = ?', vehicle_id, session['user_id'])
    if not is_users_vehicle or len(is_users_vehicle) != 1:
        return x.apology('Unauthorized access.', 'profile.vehicles')
    
    return render_template('view_vehicle.html', vehicle = is_users_vehicle[0]['img'])
    

@profilebp.route("/vehicles/modify", methods=["GET", "POST"])
@x.login_required
def modify_vehicle():
    if request.method == "POST":
        vehicle_id = request.args.get("id")
        if not vehicle_id:
            return redirect(url_for("profile.vehicles"))

        vehicle = DataBase.execute("SELECT * FROM vehicles WHERE id = ? AND user_id = ?", vehicle_id, session["user_id"])
        if len(vehicle) != 1:
            flash("Unauthorized access.")
            return redirect(url_for("profile.vehicles"))
        
        is_exist_active_req = DataBase.execute('SELECT id FROM gc_requests WHERE vehicle_id = ? AND user_id = ?', vehicle[0]['id'], session['user_id'])
        if is_exist_active_req or len(is_exist_active_req) > 0:
            return x.apology('There is an active request for this vehicle.', 'profile.vehicles')
        
        name = request.form.get("name")
        if not name or not x.valid_name(name):
            flash("Invalid name. Form refreshed.")
            return redirect(url_for("profile.modify_vehicle", id = vehicle_id))
        
        plate = request.form.get("plate")
        if not plate or not x.valid_plate(plate):
            flash("Invalid plate. Form refreshed.")
            return redirect(url_for("profile.modify_vehicle", id = vehicle_id))

        vin = request.form.get("vin")
        if not vin or not x.valid_vin(vin):
            flash("Invalid VIN. Form refreshed.")
            return redirect(url_for("profile.modify_vehicle", id = vehicle_id))

        brand = request.form.get("brand")
        if not brand or not x.valid_brand(brand):
            flash("Invalid brand. Form refreshed.")
            return redirect(url_for("profile.modify_vehicle", id = vehicle_id))

        type_ = request.form.get("type")
        if not type_ or not x.valid_type(type_):
            flash("Invalid type. Form refreshed.")
            return redirect(url_for("profile.modify_vehicle", id = vehicle_id))

        color = request.form.get("color")
        if not color or not x.valid_color(color):
            flash("Invalid color. Form refreshed.")
            return redirect(url_for("profile.modify_vehicle", id = vehicle_id))

        DataBase.execute("UPDATE vehicles SET namesurname = ?, plate = ?, vin = ?, brand = ?, model = ?, color = ? WHERE id = ?", name, plate, vin, brand, type_, color, vehicle_id)
        flash("Your vehicle have successfully modified.")
        return redirect(url_for("profile.vehicles"))
        
    else:
        vehicle_id = request.args.get("id")
        if not vehicle_id:
            return redirect(url_for("profile.vehicles"))

        vehicle = DataBase.execute("SELECT * FROM vehicles WHERE id = ? AND user_id = ?", vehicle_id, session["user_id"])
        if len(vehicle) != 1:
            flash("Unauthorized access.")
            return redirect(url_for("profile.vehicles"))

        is_exist_active_req = DataBase.execute('SELECT id FROM gc_requests WHERE vehicle_id = ? AND user_id = ?', vehicle[0]['id'], session['user_id'])
        if is_exist_active_req or len(is_exist_active_req) > 0:
            return x.apology('There is an active request for this vehicle.', 'profile.vehicles')

        return render_template("modify_vehicle.html", vehicle=vehicle[0])


@profilebp.route("/vehicles/delete", methods=['GET', 'POST'])
@x.login_required
def delete_vehicle():
    if request.method == 'POST':
        vehicle_id = request.args.get('id')
        if not vehicle_id or not vehicle_id.isdigit():
            return redirect(url_for('profile.vehicles'))
        
        vehicle_data = DataBase.execute('SELECT * FROM vehicles WHERE id = ? AND user_id = ?', vehicle_id, session['user_id'])
        if not vehicle_data or not len(vehicle_data) == 1:
            return x.apology('Unauthorized access.', 'profile.vehicles')
        
        is_exist_active_req = DataBase.execute('SELECT id FROM gc_requests WHERE vehicle_id = ? AND user_id = ?', vehicle_data[0]['id'], session['user_id'])
        if is_exist_active_req or len(is_exist_active_req) > 0:
            return x.apology('There is an active request for this vehicle.', 'profile.vehicles')
        
        user_data = DataBase.execute('SELECT * FROM users WHERE id = ?', session['user_id'])
        if not user_data or not len(user_data) == 1:
            return x.apology("Couldn't found user data, please re-login.", 'main.logout')
        
        password = request.form.get('password')
        if not password or not check_password_hash(user_data[0]['password'], password):
            return x.apology('Invalid password.', 'profile.delete_vehicle', id = vehicle_id)
        
        try:
            DataBase.execute('DELETE FROM vehicles WHERE id = ? AND user_id = ?', vehicle_id, session['user_id'])
            if os.path.exists(f'static/vehicles/{vehicle_data[0]['img']}'):
                os.remove(f'static/vehicles/{vehicle_data[0]['img']}')
            return x.apology('Your vehicle has been successfully deleted.', 'profile.vehicles')
        
        except ValueError:
            return x.apology('Error, try again.', 'profile.delete_vehicle', id = vehicle_id)

    else:
        vehicle_id = request.args.get('id')
        if not vehicle_id or not vehicle_id.isdigit():
            return redirect(url_for('profile.vehicles'))
        
        vehicle_data = DataBase.execute('SELECT * FROM vehicles WHERE id = ? AND user_id = ?', vehicle_id, session['user_id'])
        if not vehicle_data or not len(vehicle_data) == 1:
            return x.apology('Unauthorized access.', 'profile.vehicles')
        
        is_exist_active_req = DataBase.execute('SELECT id FROM gc_requests WHERE vehicle_id = ? AND user_id = ?', vehicle_data[0]['id'], session['user_id'])
        if is_exist_active_req or len(is_exist_active_req) > 0:
            return x.apology('There is an active request for this vehicle.', 'profile.vehicles')
        
        return render_template('delete_vehicle.html', vehicle_id = vehicle_data[0]['id'], plate = vehicle_data[0]['plate'])


# Pasaportlar routeunu ayarla
@profilebp.route("/passports")
@x.login_required
def passports():
    passports = DataBase.execute("SELECT * FROM passports WHERE user_id = ?", session["user_id"])
    return render_template("my_passports.html", passports=passports)


@profilebp.route("/passports/add", methods=["GET", "POST"])
@x.login_required
def add_passport():
    if request.method == "POST":
        pass_no = request.form.get("pass_no")
        if not pass_no or not x.valid_passno(pass_no):
            flash("Invalid passport number.")
            return redirect(url_for("profile.add_passport"))
        
        pass_exp = request.form.get("pass_exp")
        if not pass_exp or not x.valid_expdate(pass_exp):
            flash("Invalid date of expiry.")
            return redirect(url_for("profile.add_passport"))
        
        ident_no = request.form.get("ident_no")
        if not ident_no or not ident_no.isdigit() or len(ident_no) != 11:
            flash("Invalid identification number.")
            return redirect(url_for("profile.add_passport"))
        
        pass_img = request.files.get('pass_img')
        if not pass_img:
            return x.apology('Invalid passport image.', 'profile.add_passport')

        if not len(pass_img.filename.rsplit('.', 1)) > 1 or pass_img.filename.rsplit('.', 1)[-1].lower() not in ['jpg', 'jpeg', 'png']:
            return x.apology('Invalid passport image.', 'profile.add_passport')
        
        if not x.valid_image(pass_img):
            return x.apology('Invalid passport image.', 'profile.add_passport')

        user_data = DataBase.execute('SELECT * FROM users WHERE id = ?', session['user_id'])
        if not user_data or len(user_data) != 1:
            return x.apology('An error occurred. Please re-login.', 'main.logout')
        user = user_data[0]
        
        if user['ident_no'] != ident_no:
            flash("You are not owner of this passport.")
            return redirect(url_for("profile.add_passport"))
        
        passport = DataBase.execute("SELECT id FROM passports WHERE pass_no = ?", pass_no.upper())
        if passport:
            flash("This passport already registered in system.")
            return redirect(url_for("profile.add_passport"))

        try:
            filename = x.new_filename(pass_img.filename)
            print(filename)
            DataBase.execute("INSERT INTO passports (user_id, name, surname, sex, birth, pass_no, pass_exp, ident_no, img) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)", user['id'], user['name'].upper(), user['surname'].upper(), user['sex'], user['birth'], pass_no.upper(), x.valid_date(pass_exp), user['ident_no'], filename)
            pass_img.save(os.path.join('static', 'passports', filename))
            flash("Your passport successfully registered.")
            return redirect(url_for("profile.passports"))
        
        except ValueError:
            return x.apology('Error. Try again.', 'profile.add_passport')
        
    else:
        return render_template("add_passport.html")
    

@profilebp.route('/passports/view')
@x.login_required
def view_passport():
    pass_id = request.args.get('id')
    if not pass_id or not pass_id.isdigit():
        return redirect('profile.passports')
    
    is_users_pass = DataBase.execute('SELECT * FROM passports WHERE id = ? AND user_id = ?', pass_id, session['user_id'])
    if not is_users_pass or len(is_users_pass) != 1:
        return x.apology('Unauthorized access.', 'profile.passports')
    
    return render_template('view_passport.html', passport = is_users_pass[0]['img'])


@profilebp.route("/passports/modify", methods = ["GET", "POST"])
@x.login_required
def modify_passport():
    if request.method == "POST":
        passport_id = request.args.get("id")
        if not passport_id:
            return redirect(url_for('profile.passports'))
        
        passport = DataBase.execute("SELECT * FROM passports WHERE user_id = ? AND id = ?", session["user_id"], passport_id)
        if not passport:
            flash("Unauthorized access.")
            return redirect(url_for('profile.passports'))
        
        if passport[0]['confirmed'] != 0:
            return x.apology("The confirmed passport cannot be modify.", 'profile.passports')
        
        passport_active_req = DataBase.execute(x.file_query('passport_active_request.sql'), session['user_id'], passport_id)
        if passport_active_req:
            return x.apology('The deletion process cannot be completed because there is an active application.', 'profile.passports')

        pass_exp = request.form.get('pass_exp')
        if not pass_exp or not x.valid_date(pass_exp):
            return x.apology('Invalid passport number. Form refreshed.', 'profile.modify_passport', id = passport_id)
        
        try:
            DataBase.execute('UPDATE passports SET pass_exp = ? WHERE user_id = ? AND id = ?', x.valid_date(pass_exp), session['user_id'], passport_id)
            return x.apology('Your passport has successfully modified.', 'profile.passports')

        except ValueError:
            return x.apology('Error, try again.', 'profile.modify_passport', id = passport_id)
        
    else:
        passport_id = request.args.get("id")
        if not passport_id:
            return redirect(url_for('profile.passports'))

        passport = DataBase.execute('SELECT * FROM passports WHERE id = ? AND user_id = ?', passport_id, session['user_id'])
        if len(passport) != 1:
            return x.apology('Unauthorized access.', 'profile.passports')
        
        if passport[0]['confirmed'] != 0:
            return x.apology('The confirmed passport cannot be modify.', 'profile.passports')
        
        passport_active_req = DataBase.execute(x.file_query('passport_active_request.sql'), session['user_id'], passport_id)
        if passport_active_req:
            return x.apology('The deletion process cannot be completed because there is an active application.', 'profile.passports')
        
        passport[0]['birth'] = datetime.strptime(passport[0]['birth'], '%d/%m/%Y').strftime('%Y-%m-%d')
        passport[0]['pass_exp'] = datetime.strptime(passport[0]['pass_exp'], '%d/%m/%Y').strftime('%Y-%m-%d')

        return render_template("modify_passport.html", passport=passport[0])


@profilebp.route("/passports/delete", methods=["GET", "POST"])
@x.login_required
def delete_passport():
    if request.method == "POST":
        passport_id = request.args.get('id')
        if not passport_id:
            return redirect(url_for('profiles.passports'))

        passport = DataBase.execute('SELECT * FROM passports WHERE id = ? AND user_id = ?', passport_id, session['user_id'])
        if not passport or len(passport) != 1:
            return x.apology('Unauthorized access.', 'profile.passports')

        passport_active_req = DataBase.execute(x.file_query('passport_active_request.sql'), session['user_id'], passport_id)
        if passport_active_req:
            return x.apology('The deletion process cannot be completed because there is an active application.', 'profile.passports')
        
        user_data = DataBase.execute('SELECT * FROM users WHERE id = ?', session['user_id'])
        if not user_data:
            return x.apology('Please relogin.', 'main.logout')
        
        cur_password = user_data[0]['password']

        password = request.form.get('password')
        if not password or not check_password_hash(cur_password, password):
            return x.apology('Invalid password.', 'profile.delete_passport', id = passport_id)
            
        try:
            DataBase.execute('DELETE FROM passports WHERE id = ? AND user_id = ?', passport[0]['id'], session['user_id'])
            if os.path.exists(f'static/passports/{passport[0]['img']}'):
                os.remove(f'static/passports/{passport[0]['img']}')
            return x.apology('Your passport successfully deleted.', 'profile.passports')

        except ValueError:
            return x.apology('Error. Try again.', 'profile.passports')
        
    else:
        passport_id = request.args.get('id')
        if not passport_id or not passport_id.isdigit():
            return redirect(url_for('profile.passports'))
        
        passport_data = DataBase.execute('SELECT * FROM passports WHERE id = ? AND user_id = ?', passport_id, session['user_id'])
        if not len(passport_data) == 1:
            return x.apology('Unauthorized access.', 'profile.passports')
        
        passport_active_req = DataBase.execute(x.file_query('passport_active_request.sql'), session['user_id'], passport_id)
        if passport_active_req:
            return x.apology('The deletion process cannot be completed because there is an active application.', 'profile.passports')

        return render_template('delete_passport.html', passport_id=passport_data[0]['id'], passport_no=passport_data[0]['pass_no'])