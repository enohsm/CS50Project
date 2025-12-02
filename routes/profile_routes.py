from .imports import *


# ENG: Assign a variable for the profile routes blueprint
# TR: Profil rotalarını modülleyecek bir değişken ata
profilebp = Blueprint("profile", __name__, url_prefix="/me")

# ENG: Profile route
# TR: Profil rotası
@profilebp.route("/")
@x.login_required
def profile():
    user_data = DataBase.execute('SELECT username, name, surname, sex, birth, ident_no, email, contact FROM users WHERE id = ?', session['user_id'])
    if not user_data or len(user_data) != 1:
        return x.apology('Profile could not loaded. Please try again.', 'main.homepage')
    return render_template("profile.html", user = user_data[0])


# ENG: Vehicles route
# TR: Araçlar rotası
@profilebp.route("/vehicles")
@x.login_required
def vehicles():
    # ENG: Get user's vehicles
    # TR: Kullanıcıya ait araçları sorgula
    vehicles = DataBase.execute("SELECT * FROM vehicles WHERE user_id = ?", session["user_id"])
    return render_template("my_vehicles.html", vehicles=vehicles)


# ENG: Add vehicle route
# TR: Araç ekleme rotası
@profilebp.route("/vehicles/add", methods=["GET", "POST"])
@x.login_required
def add_vehicle():
    if request.method == "POST":
        # ENG: Get data from form
        # TR: Formdan verileri al
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

        # ENG: Get vehicle image from form
        # TR: Ruhsat görüntüsünü formdan al
        vehicle_img = request.files.get('vehicle_img')
        if not vehicle_img:
            return x.apology('Invalid vehicle image.', 'profile.add_vehicle')

        # ENG: Check if image is valid
        # TR: Geçerli bir görüntü dosyası mı kontrol et
        if not x.valid_image(vehicle_img):
            return x.apology('Invalid vehicle image.', 'profile.add_vehicle')
    
        # ENG: Check extension exists
        # TR: Uzantısı var mı kontrol et
        if not len(vehicle_img.filename.rsplit('.', 1)) > 1:
            return x.apology('Invalid vehicle image.', 'profile.add_vehicle')
        
        # ENG: Check extension is allowed
        # TR: Uzantısı geçerli mi kontrol et
        if vehicle_img.filename.lower().rsplit('.', 1)[-1] not in ['jpg', 'jpeg', 'png']:
            return x.apology('Invalid vehicle image.', 'profile.add_vehicle')

        # ENG: Check if vehicle already exists
        # TR: Kullanıcının araçlarında böyle bir araç mevcut mu kontrol et (plaka ve şase numarası ile)
        vehicle = DataBase.execute("SELECT id FROM vehicles WHERE user_id = ? AND plate = ? OR vin = ?", session["user_id"], plate, vin)
        if vehicle:
            flash("This vehicle is already in your vehicle list.")
            return redirect(url_for("profile.add_vehicle"))
        
        # ENG: Add vehicle
        # TR: Aracı ekle
        try:
            # ENG: Create safe filename
            # TR: Güvenli bir dosya adı oluştur
            filename = x.new_filename(vehicle_img.filename)

            # ENG: Insert into database
            # TR: Veritabanına ekle
            DataBase.execute("INSERT INTO vehicles (user_id, namesurname, address, plate, vin, brand, model, color, img) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)", session["user_id"], name.upper(), (district.upper()+"/"+province.upper()), plate.upper(), vin.upper(), brand.upper(), type.upper(), color.upper(), filename)
            
            # ENG: Create folder if not exists
            # TR: 'Araçlar' klasörü yok ise oluştur
            os.makedirs(os.path.join('static', 'vehicles'), exist_ok=True)

            # ENG: Save image
            # TR: Görüntüyü kaydet
            vehicle_img.save(os.path.join('static', 'vehicles', filename))

            flash("Your vehicle has successfully registered.")
            return redirect(url_for("profile.vehicles"))
        
        except ValueError:
            return x.apology('An error occurred. Please try again.', 'profile.add_vehicle')
        
    else:
        return render_template("add_vehicle.html")
    

# ENG: View vehicle image
# TR: Araç ruhsatı görüntüleme
@profilebp.route('/vehicles/view')
@x.login_required
def view_vehicle():
    vehicle_id = request.args.get('id')
    if not vehicle_id or not vehicle_id.isdigit():
        return redirect('profile.vehicles')
    
    license_img = []

    # ENG: Check ownership for normal user
    # TR: Eğer rol kullanıcıysa:
    if session['role'] < 1:

        # ENG: Check ownership
        # TR: Kullanıcı bu araca sahip mi kontrol et
        is_users_vehicle = DataBase.execute('SELECT * FROM vehicles WHERE id = ? AND user_id = ?', vehicle_id, session['user_id'])
        if not is_users_vehicle or len(is_users_vehicle) != 1:
            return x.apology('Unauthorized access.', 'profile.vehicles')
        license_img = is_users_vehicle

    # ENG: Check license by ID for staff/admin
    # TR: Eğer çalışan ya da admin ise:
    elif session['role'] >= 1:

        # ENG: Query vehicle directly by ID
        # TR: Ruhsatı direkt id ile sorgula
        is_vehicle = DataBase.execute('SELECT * FROM vehicles WHERE id = ?', vehicle_id)
        if not is_vehicle or len(is_vehicle) != 1:
            return x.apology('Unauthorized access.', 'profile.vehicles')
        license_img = is_vehicle
    
    return render_template('view_vehicle.html', vehicle = license_img[0]['img'])
    

# ENG: Modify vehicle route
# TR: Araç düzenleme rotası
@profilebp.route("/vehicles/modify", methods=["GET", "POST"])
@x.login_required
def modify_vehicle():
    if request.method == "POST":
        vehicle_id = request.args.get("id")
        if not vehicle_id:
            return redirect(url_for("profile.vehicles"))

        # ENG: Check ownership
        # TR: Kullanıcı bu araca sahip mi kontrol et
        vehicle = DataBase.execute("SELECT * FROM vehicles WHERE id = ? AND user_id = ?", vehicle_id, session["user_id"])
        if len(vehicle) != 1:
            flash("Unauthorized access.")
            return redirect(url_for("profile.vehicles"))
        
        # ENG: Active request exists?
        # TR: Bu araca ait halihazırda bekleyen bir talep mevcut mu?
        is_exist_active_req = DataBase.execute('SELECT id FROM gc_requests WHERE vehicle_id = ? AND user_id = ?', vehicle[0]['id'], session['user_id'])
        if is_exist_active_req or len(is_exist_active_req) > 0:
            return x.apology('There is an active request for this vehicle.', 'profile.vehicles')
        
        # ENG: Get data from form
        # TR: Formdan verileri al
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

        # ENG: Update vehicle
        # TR: Aracı güncelle
        try:
            DataBase.execute("UPDATE vehicles SET namesurname = ?, plate = ?, vin = ?, brand = ?, model = ?, color = ? WHERE id = ?", name, plate, vin, brand, type_, color, vehicle_id)
            flash("Your vehicle have successfully modified.")
            return redirect(url_for("profile.vehicles"))
        
        except ValueError:
            return x.apology('An error occurred, please try again.', 'profile.modify_vehicle', id = vehicle_id)
        
    else:
        vehicle_id = request.args.get("id")
        if not vehicle_id:
            return redirect(url_for("profile.vehicles"))

        # ENG: Check ownership
        # TR: Kullanıcı bu araca sahip mi kontrol et
        vehicle = DataBase.execute("SELECT * FROM vehicles WHERE id = ? AND user_id = ?", vehicle_id, session["user_id"])
        if len(vehicle) != 1:
            flash("Unauthorized access.")
            return redirect(url_for("profile.vehicles"))

        # ENG: Active request exists?
        # TR: Bu araç için halihazırda aktif bir talep mevcut mu?
        is_exist_active_req = DataBase.execute('SELECT id FROM gc_requests WHERE vehicle_id = ? AND user_id = ?', vehicle[0]['id'], session['user_id'])
        if is_exist_active_req or len(is_exist_active_req) > 0:
            return x.apology('There is request(s) for this vehicle. You can delete this vehicle and add again this one.', 'profile.vehicles')

        return render_template("modify_vehicle.html", vehicle=vehicle[0])


# ENG: Delete vehicle route
# TR: Aracı silme rotası
@profilebp.route("/vehicles/delete", methods=['GET', 'POST'])
@x.login_required
def delete_vehicle():
    if request.method == 'POST':
        vehicle_id = request.args.get('id')
        if not vehicle_id or not vehicle_id.isdigit():
            return redirect(url_for('profile.vehicles'))
        
        # ENG: Check ownership
        # TR: Kullanıcı bu araca sahip mi kontrol et
        vehicle_data = DataBase.execute('SELECT * FROM vehicles WHERE id = ? AND user_id = ?', vehicle_id, session['user_id'])
        if not vehicle_data or not len(vehicle_data) == 1:
            return x.apology('Unauthorized access.', 'profile.vehicles')
        
        # ENG: Active request exists?
        # TR: Bu araç için halihazırda aktif başvuru var mı kontrol et
        is_exist_active_req = DataBase.execute('SELECT id FROM gc_requests WHERE vehicle_id = ? AND user_id = ? AND status != 2', vehicle_data[0]['id'], session['user_id'])
        if is_exist_active_req or len(is_exist_active_req) > 0:
            return x.apology('There is an active request for this vehicle.', 'profile.vehicles')
        
        # ENG: Retrieve user data from the database for password verification
        # TR: Kullanıcı şifresi için veritabanından kullanıcı bilgilerini al
        user_data = DataBase.execute('SELECT * FROM users WHERE id = ?', session['user_id'])
        if not user_data or not len(user_data) == 1:
            return x.apology("Couldn't found user data, please re-login.", 'main.logout')
        
        # ENG: Get the password from the form and validate
        # TR: Kullanıcı şifresini formdan al ve doğrulama yap
        password = request.form.get('password')
        if not password or not check_password_hash(user_data[0]['password'], password):
            return x.apology('Invalid password.', 'profile.delete_vehicle', id = vehicle_id)
        
        # ENG: Delete the vehicle
        # TR: Aracı sil
        try:
            # ENG: Delete all past insurance requests for the vehicle from the database
            # TR: Araca dair geçmiş tüm sigorta başvurularını veritabanından sil
            DataBase.execute('DELETE FROM gc_requests WHERE vehicle_id = ? AND user_id = ?', vehicle_id, session['user_id'])

            # ENG: Delete the vehicle from the database
            # TR: Aracı veritabanından sil
            DataBase.execute('DELETE FROM vehicles WHERE id = ? AND user_id = ?', vehicle_id, session['user_id'])

            # ENG: Delete the vehicle image if it exists
            # TR: Ruhsat görüntüsü mevcut ise veritabanından sil
            if os.path.exists(f"static/vehicles/{vehicle_data[0]['img']}"):
                os.remove(f"static/vehicles/{vehicle_data[0]['img']}")

            return x.apology('Your vehicle has been successfully deleted.', 'profile.vehicles')
        
        except ValueError:
            return x.apology('Error, try again.', 'profile.delete_vehicle', id = vehicle_id)

    else:
        vehicle_id = request.args.get('id')
        if not vehicle_id or not vehicle_id.isdigit():
            return redirect(url_for('profile.vehicles'))
        
        # ENG: Check ownership
        # TR: Kullanıcı bu araca sahip mi kontrol et
        vehicle_data = DataBase.execute('SELECT * FROM vehicles WHERE id = ? AND user_id = ?', vehicle_id, session['user_id'])
        if not vehicle_data or not len(vehicle_data) == 1:
            return x.apology('Unauthorized access.', 'profile.vehicles')
        
        # ENG: Active request exists?
        # TR: Bu aracın aktif bir talebi olup olmadığını kontrol et
        is_exist_active_req = DataBase.execute('SELECT id FROM gc_requests WHERE vehicle_id = ? AND user_id = ? AND status != 2', vehicle_data[0]['id'], session['user_id'])
        if is_exist_active_req or len(is_exist_active_req) > 0:
            return x.apology('There is an active request for this vehicle.', 'profile.vehicles')
        
        return render_template('delete_vehicle.html', vehicle_id = vehicle_data[0]['id'], plate = vehicle_data[0]['plate'])


# ENG: Passports route
# TR: Pasaportlar rotası
@profilebp.route("/passports")
@x.login_required
def passports():
    passports = DataBase.execute("SELECT * FROM passports WHERE user_id = ?", session["user_id"])
    return render_template("my_passports.html", passports=passports)


# ENG: Add passport route
# TR: Pasaport ekleme rotası
@profilebp.route("/passports/add", methods=["GET", "POST"])
@x.login_required
def add_passport():
    if request.method == "POST":

        # ENG: Get data from form
        # TR: Formdan verileri al
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
        
        # ENG: Get the passport image from the form
        # TR: Pasaport görüntüsünü formdan al
        pass_img = request.files.get('pass_img')
        if not pass_img:
            return x.apology('Invalid passport image.', 'profile.add_passport')

        # ENG: Check if the filename is valid (has an extension and the extension is valid)
        # TR: Görüntü dosyasının ismi geçerli mi kontrol et (uzantı var mı ya da uzantı geçerli mi)
        if not len(pass_img.filename.rsplit('.', 1)) > 1 or pass_img.filename.rsplit('.', 1)[-1].lower() not in ['jpg', 'jpeg', 'png']:
            return x.apology('Invalid passport image.', 'profile.add_passport')
        
        # ENG: Validate the image file
        # TR: Görüntü geçerli mi kontrol et
        if not x.valid_image(pass_img):
            return x.apology('Invalid passport image.', 'profile.add_passport')

        # ENG: Retrieve user data from the database for password verification
        # TR: Kullanıcı bilgilerini şifre için veritabanından al
        user_data = DataBase.execute('SELECT * FROM users WHERE id = ?', session['user_id'])
        if not user_data or len(user_data) != 1:
            return x.apology('An error occurred. Please re-login.', 'main.logout')
        user = user_data[0]
        
        # ENG: Check user identity with passport
        # TR: Pasaport üzerindeki kimlik numarası ile kullanıcının kimlik numarası eşleşiyor mu kontrol et
        if user['ident_no'] != ident_no:
            flash("You are not owner of this passport.")
            return redirect(url_for("profile.add_passport"))
        
        # ENG: Check if passport with this number already exists
        # TR: Bu pasaport numarasıyla kayıtlı bir pasaport mevcut mu kontrol et
        passport = DataBase.execute("SELECT id FROM passports WHERE pass_no = ?", pass_no.upper())
        if passport:
            flash("This passport already registered in system.")
            return redirect(url_for("profile.add_passport"))

        # ENG: Save passport
        # TR: Pasaportu kaydet
        try:
            # ENG: Create safe filename
            # TR: Güvenli bir dosya ismi oluştur
            filename = x.new_filename(pass_img.filename)

            # ENG: Insert into database
            # TR: Pasaport bilgilerini veritabanına kaydet
            DataBase.execute("INSERT INTO passports (user_id, name, surname, sex, birth, pass_no, pass_exp, ident_no, img) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)", user['id'], user['name'].upper(), user['surname'].upper(), user['sex'], user['birth'], pass_no.upper(), x.valid_date(pass_exp), user['ident_no'], filename)
            
            # ENG: Create folder if not exists
            # TR: Klasör yoksa klasörü oluştur
            os.makedirs(os.path.join('static', 'vehicles'), exist_ok=True)

            # ENG: Save image
            # TR: Pasaport görüntüsünü kaydet
            pass_img.save(os.path.join('static', 'passports', filename))

            flash("Your passport successfully registered.")
            return redirect(url_for("profile.passports"))
        
        except ValueError:
            return x.apology('Error. Try again.', 'profile.add_passport')
        
    else:
        return render_template("add_passport.html")
    

# ENG: Route for viewing passport image
# TR: Pasaport görüntüleme rotası
@profilebp.route('/passports/view')
@x.login_required
def view_passport():
    pass_id = request.args.get('id')
    if not pass_id or not pass_id.isdigit():
        return redirect('profile.passports')
    
    passport_img = []

    # ENG: Check ownership for normal user
    # TR: Eğer rol kullanıcıysa:
    if session['role'] < 1:

        # ENG: Check if passport belongs to user
        # TR: Pasaport kullanıcıya mı ait sorgula
        is_users_pass = DataBase.execute('SELECT * FROM passports WHERE id = ? AND user_id = ?', pass_id, session['user_id'])
        if not is_users_pass or len(is_users_pass) != 1:
            return x.apology('Unauthorized access.', 'profile.passports')
        passport_img = is_users_pass

    
    # ENG: Check passport by ID for staff/admin
    # TR: Eğer çalışan ya da admin ise:
    elif session['role'] >= 1:

        # ENG: Query passport directly by ID
        # TR: Pasaportu direkt id ile sorgula
        is_pass = DataBase.execute('SELECT * FROM passports WHERE id = ?', pass_id)
        if not is_pass or len(is_pass) != 1:
            return x.apology('Passport image could not found.', 'dashboard.passport_confirmation')
        passport_img = is_pass
    
    return render_template('view_passport.html', passport = passport_img[0]['img'])


# ENG: Route for modifying passport
# TR: Pasaport düzenleme rotası
@profilebp.route("/passports/modify", methods = ["GET", "POST"])
@x.login_required
def modify_passport():
    if request.method == "POST":
        passport_id = request.args.get("id")
        if not passport_id:
            return redirect(url_for('profile.passports'))
        
        # ENG: Check ownership
        # TR: Kullanıcı bu pasaporta sahip mi kontrol et
        passport = DataBase.execute("SELECT * FROM passports WHERE user_id = ? AND id = ?", session["user_id"], passport_id)
        if not passport:
            flash("Unauthorized access.")
            return redirect(url_for('profile.passports'))
        
        # ENG: Check if passport is already confirmed
        # TR: Kullanıcının pasaportu onaylanmış mı kontrol et
        if passport[0]['confirmed'] != 0:
            return x.apology("The confirmed passport cannot be modify.", 'profile.passports')
        
        # ENG: Check if active application exists
        # TR: Pasaportun hali hazırda akitf bir başvurusu var mı kontrol et
        passport_active_req = DataBase.execute(x.file_query('passport_active_request.sql'), session['user_id'], passport_id)
        if passport_active_req:
            return x.apology('The deletion process cannot be completed because there is an active application.', 'profile.passports')

        # ENG: Get data from form
        # TR: Formdan veriyi al
        pass_exp = request.form.get('pass_exp')
        if not pass_exp or not x.valid_date(pass_exp):
            return x.apology('Invalid passport number. Form refreshed.', 'profile.modify_passport', id = passport_id)
        
        # ENG: Save modified passport
        # TR: Düzenlenmiş pasaportu kaydet
        try:
            DataBase.execute('UPDATE passports SET pass_exp = ? WHERE user_id = ? AND id = ?', x.valid_date(pass_exp), session['user_id'], passport_id)
            return x.apology('Your passport has successfully modified.', 'profile.passports')

        except ValueError:
            return x.apology('Error, try again.', 'profile.modify_passport', id = passport_id)
        
    else:
        passport_id = request.args.get("id")
        if not passport_id:
            return redirect(url_for('profile.passports'))

        # ENG: Check if user owns this passport
        # TR: Kullanıcının böyle bir pasaportu var mı kontrol et
        passport = DataBase.execute('SELECT * FROM passports WHERE id = ? AND user_id = ?', passport_id, session['user_id'])
        if len(passport) != 1:
            return x.apology('Unauthorized access.', 'profile.passports')
        
        # ENG: Check if confirmed
        # TR: Onaylanıp onaylanmadığını kontrol et
        if passport[0]['confirmed'] != 0:
            return x.apology('The confirmed passport cannot be modify.', 'profile.passports')
        
        # ENG: Check for active applications
        # TR: Aktif başvurusu var mı kontrol et
        passport_active_req = DataBase.execute(x.file_query('passport_active_request.sql'), session['user_id'], passport_id)
        if passport_active_req:
            return x.apology('The deletion process cannot be completed because there is an active application.', 'profile.passports')
        
        # ENG: Reformat dates for form
        # TR: Veritabanındaki tarih verilerini form'a yazacağımız için yeniden formatlıyoruz
        passport[0]['birth'] = datetime.strptime(passport[0]['birth'], '%d/%m/%Y').strftime('%Y-%m-%d')
        passport[0]['pass_exp'] = datetime.strptime(passport[0]['pass_exp'], '%d/%m/%Y').strftime('%Y-%m-%d')

        return render_template("modify_passport.html", passport=passport[0])

# ENG: Route for deleting passport
# TR: Pasaport silme rotası
@profilebp.route("/passports/delete", methods=["GET", "POST"])
@x.login_required
def delete_passport():
    if request.method == "POST":
        passport_id = request.args.get('id')
        if not passport_id:
            return redirect(url_for('profiles.passports'))

        # ENG: Check ownership
        # TR: Kullanıcı pasaporta sahip mi?
        passport = DataBase.execute('SELECT * FROM passports WHERE id = ? AND user_id = ?', passport_id, session['user_id'])
        if not passport or len(passport) != 1:
            return x.apology('Unauthorized access.', 'profile.passports')

        # ENG: Check for active applications
        # TR: Pasaporta ait aktif başvuru var mı?
        passport_active_req = DataBase.execute(x.file_query('passport_active_request.sql'), session['user_id'], passport_id)
        if passport_active_req:
            return x.apology('The deletion process cannot be completed because there is an active application.', 'profile.passports')
        
        # ENG: Retrieve user data for password check
        # TR: Kullanıcı verisini şifre için al
        user_data = DataBase.execute('SELECT * FROM users WHERE id = ?', session['user_id'])
        if not user_data:
            return x.apology('Please relogin.', 'main.logout')
        
        # ENG: Store current password
        # TR: Satır sütun ile işlemi kolaylaştırmak adına şifreyi bir değişkene al
        cur_password = user_data[0]['password']

        # ENG: Get password from form
        # TR: Formdan veriyi (şifreyi) al
        password = request.form.get('password')
        if not password or not check_password_hash(cur_password, password):
            return x.apology('Invalid password.', 'profile.delete_passport', id = passport_id)
        
        # ENG: Delete passport
        # TR: Pasaportu sil
        try:
            
            # ENG: Delete related references
            # TR: Pasaporta ait referans numaralarını sil (Çalışan dashboardında göreceksiniz)
            DataBase.execute('DELETE FROM app_references WHERE pass_id = ?', passport[0]['id'])

            # ENG: Delete all past visa requests for this passport
            # TR: Pasaporta ait geçmiş tüm vize taleplerini sil
            DataBase.execute('DELETE FROM visa_requests WHERE pass_id = ? AND user_id = ?', passport[0]['id'], session['user_id'])

            # ENG: Delete passport from database
            # TR: Pasaport verilerini veritabanından sil
            DataBase.execute('DELETE FROM passports WHERE id = ? AND user_id = ?', passport[0]['id'], session['user_id'])

            # ENG: Delete passport image if exists
            # TR: Pasaport görüntüsü mevcut ise pasaport görüntüsünü sil
            if os.path.exists(f'static/passports/{passport[0]['img']}'):
                os.remove(f'static/passports/{passport[0]['img']}')

            return x.apology('Your passport successfully deleted.', 'profile.passports')

        except ValueError:
            return x.apology('Error. Try again.', 'profile.passports')
        
    else:
        passport_id = request.args.get('id')
        if not passport_id or not passport_id.isdigit():
            return redirect(url_for('profile.passports'))
        
        # ENG: Check ownership
        # TR: Kullanıcı bu pasaporta sahip mi?
        passport_data = DataBase.execute('SELECT * FROM passports WHERE id = ? AND user_id = ?', passport_id, session['user_id'])
        if not len(passport_data) == 1:
            return x.apology('Unauthorized access.', 'profile.passports')
        
        # ENG: Check for active applications
        # TR: Bu pasaporta ait aktif başvuru mevcut mu?
        passport_active_req = DataBase.execute(x.file_query('passport_active_request.sql'), session['user_id'], passport_id)
        if passport_active_req:
            return x.apology('The deletion process cannot be completed because there is an active application.', 'profile.passports')

        return render_template('delete_passport.html', passport_id=passport_data[0]['id'], passport_no=passport_data[0]['pass_no'])


# ENG: Route for changing password
# TR: Şifre değiştirme rotası
@profilebp.route('changepassword', methods = ['GET', 'POST'])
@x.login_required()
def change_password():
    if request.method == 'POST':
        # ENG: Retrieve user password
        # TR: Kullanıcı bilgilerini sorgula
        user_data = DataBase.execute('SELECT password FROM users WHERE id = ?', session['user_id'])
        if not user_data or len(user_data) != 1:
            return x.apology('User data could not found.', 'main.logout')

        # ENG: Current password
        # TR: Kullanıcının şifresini bir değişkene koy
        cur_pass = user_data[0]['password']

        # ENG: Check old password
        # TR: Formdan eski şifreyi al ve eşleşmeyi kontrol et
        old_pass = request.form.get('old_pass')
        if not old_pass or not check_password_hash(cur_pass, old_pass):
            return x.apology('Invalid old password.', 'profile.change_password')

        # ENG: Get new password and confirmation
        # TR: Yeni şifreyi ve onayı formdan al, eşleşmezlerse hata döndür
        password = request.form.get('password')
        confirmation = request.form.get('confirmation')
        if not password or not confirmation or password != confirmation:
            return x.apology('New passwords not matching.', 'profile.change_password')
        
        # ENG: Old and new password cannot be same
        # TR: Eski şifreyle yeni şifre aynı olamaz
        if password == old_pass:
            return x.apology('Old password and new password cannot be same.', 'profile.change_password')

        # ENG: Validate new password
        # TR: Geçerli şifre kontrolü
        if not x.valid_password(password):
            return x.apology('New password is invalid.', 'profile.change_password')

        # ENG: Update password
        # TR: Şifreyi güncelle
        try:
            DataBase.execute('UPDATE users SET password = ? WHERE id = ?', generate_password_hash(password), session['user_id'])
            return x.apology('Your password has been successfully changed.', 'main.homepage')
        
        except ValueError:
            return x.apology('An error occurred, please try again.', 'profile.change_password')

    else:
        return render_template('change_password.html')