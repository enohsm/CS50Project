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
        
        vehicle = DataBase.execute("SELECT id FROM vehicles WHERE user_id = ? AND plate = ? OR vin = ?", session["user_id"], plate, vin)
        if vehicle:
            flash("This vehicle is already in your vehicle list.")
            return redirect(url_for("profile.add_vehicle"))
        
        DataBase.execute("INSERT INTO vehicles (user_id, namesurname, address, plate, vin, brand, model, color) VALUES(?, ?, ?, ?, ?, ?, ?, ?)", session["user_id"], name.upper(), (district.upper()+"/"+province.upper()), plate.upper(), vin.upper(), brand.upper(), type.upper(), color.upper())
        flash("Your vehicle has successfully registered.")
        return redirect(url_for("profile.vehicles"))
    else:
        return render_template("add_vehicle.html")
    

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
        
        user_data = DataBase.execute('SELECT * FROM users WHERE id = ?', session['user_id'])
        if not user_data or not len(user_data) == 1:
            return x.apology("Couldn't found user data, please re-login.", 'main.logout')
        
        password = request.form.get('password')
        if not password or not check_password_hash(user_data[0]['password'], password):
            return x.apology('Invalid password.', 'profile.delete_vehicle', id = vehicle_id)
        
        try:
            DataBase.execute('DELETE FROM vehicles WHERE id = ? AND user_id = ?', vehicle_id, session['user_id'])
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
        name = request.form.get("name")
        surname = request.form.get("surname")
        if not name or not surname or not x.valid_name((name + " " + surname)):
            flash("Invalid name/surname.")
            return redirect(url_for("profile.add_passport"))
        
        sex = request.form.get("sex")
        if not sex or sex not in ["male", "female"]:
            flash("Invalid sex.")
            return redirect(url_for("profile.add_passport"))
        
        birth = request.form.get("birth")
        if not birth or not x.valid_date(birth):
            flash("Invalid birth date.")
            return redirect(url_for("profile.add_passport"))
        
        pass_no = request.form.get("pass_no")
        if not pass_no or not x.valid_passno(pass_no):
            flash("Invalid passport number.")
            return redirect(url_for("profile.add_passport"))
        
        pass_exp = request.form.get("pass_exp")
        if not pass_exp or not x.valid_date(pass_exp):
            flash("Invalid date of expiry.")
            return redirect(url_for("profile.add_passport"))
        
        ident_no = request.form.get("ident_no")
        if not ident_no or not ident_no.isdigit() or len(ident_no) != 11:
            flash("Invalid identification number.")
            return redirect(url_for("profile.add_passport"))
        
        user_ident_no = DataBase.execute("SELECT ident_no FROM users WHERE id = ?", session["user_id"])[0]["ident_no"]
        if user_ident_no != ident_no:
            flash("You are not owner of this passport.")
            return redirect(url_for("profile.add_passport"))
        
        passport = DataBase.execute("SELECT id FROM passports WHERE pass_no = ?", pass_no)
        if passport:
            flash("This passport already registered in system.")
            return redirect(url_for("profile.add_passport"))
        
        try:
            DataBase.execute("INSERT INTO passports (user_id, name, surname, sex, birth, pass_no, pass_exp, ident_no) VALUES(?, ?, ?, ?, ?, ?, ?, ?)", session["user_id"], name.upper(), surname.upper(), sex.upper(), x.valid_date(birth), pass_no.upper(), x.valid_date(pass_exp), ident_no)
            flash("Your passport successfully registered.")
            return redirect(url_for("profile.passports"))
        except ValueError:
            return x.apology('Error. Try again.', 'profile.add_passport')
    else:
        return render_template("add_passport.html")


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
        
        name = request.form.get("name")
        surname = request.form.get("surname")
        if not name or not x.valid_name(name + " " + surname):
            return x.apology('Invalid name or surname. Form refreshed.', 'profile.modify_passport', id = passport_id)
        
        sex = request.form.get("sex")
        if not sex or sex not in ["male", "female"]:
            return x.apology('Invalid sex. Form refreshed', 'profile.modify_passport', id = passport_id)
        
        birth = request.form.get('birth')
        if not birth or not x.valid_date(birth):
            return x.apology('Invalid birth date. Form refreshed.', 'profile.modify_passport', id = passport_id)
        
        pass_no = request.form.get('pass_no')
        if not pass_no or not x.valid_passno(pass_no):
            return x.apology('Invalid passport number. Form refreshed.', 'profile.modify_passport', id = passport_id)

        pass_exp = request.form.get('pass_exp')
        if not pass_exp or not x.valid_date(pass_exp):
            return x.apology('Invalid passport number. Form refreshed.', 'profile.modify_passport', id = passport_id)
        
        ident_no = request.form.get('ident_no')
        if not ident_no or not ident_no.isdigit() or len(ident_no) != 11:
            return x.apology('Invalid identification number. Form refreshed.', 'profile.modify_passport', id = passport_id)
        
        isexist = DataBase.execute('SELECT * FROM passports WHERE pass_no = ? AND user_id != ?', pass_no, session['user_id'])
        if isexist:
            return x.apology('This passport is already registered in the system.', 'profile.modify_passport', id = passport_id)
        
        try:
            DataBase.execute('UPDATE passports SET name = ?, surname = ?, sex = ?, birth = ?, pass_no = ?, pass_exp = ?, ident_no = ? WHERE user_id = ? AND id = ?', name.upper(), surname.upper(), sex.upper(), x.valid_date(birth), pass_no.upper(), x.valid_date(pass_exp), ident_no, session['user_id'], passport_id)
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

        passport = DataBase.execute('SELECT id FROM passports WHERE id = ? AND user_id = ?', passport_id, session['user_id'])
        if not passport or len(passport) != 1:
            return x.apology('Unauthorized access.', 'profile.passports')
        
        user_data = DataBase.execute('SELECT * FROM users WHERE id = ?', session['user_id'])
        if not user_data:
            return x.apology('Please relogin.', 'main.logout')
        
        cur_password = user_data[0]['password']

        password = request.form.get('password')
        if not password or not check_password_hash(cur_password, password):
            return x.apology('Invalid password.', 'profile.delete_passport', id = passport_id)
            
        try:
            DataBase.execute('DELETE FROM passports WHERE id = ? AND user_id = ?', passport[0]['id'], session['user_id'])
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

        return render_template('delete_passport.html', passport_id=passport_data[0]['id'], passport_no=passport_data[0]['pass_no'])


# Evraklar routeunu ayarla
@profilebp.route("/documents")
@x.login_required
def documents():
    return render_template("my_documents.html")


# Requests routeunu ayarla
@profilebp.route("/requests")
@x.login_required
def requests():
    # Kullanıcının son 10 adet vize başvuru taleplerini sorgula (request_time DESC)
    visa_requests = DataBase.execute('SELECT * FROM visa_requests WHERE user_id = ?', session['user_id'])

    # Kullanıcının son 10 adet yeşil sigorta taleplerini sorgula (request_time DESC)
    gc_requests = DataBase.execute('SELECT * FROM gc_requests WHERE user_id = ?', session['user_id'])

    return render_template("my_requests.html", visa = visa_requests, greencard = gc_requests)


# Vize randevu talebi oluşturma route'unu ayarla
@profilebp.route('/request/visa/new', methods=['GET', 'POST'])
@x.login_required
def new_visa_request():
    if request.method == 'POST':
        # Pasaport numarasını formdan al
        pass_no = request.form.get('pass_no')
        if not pass_no or not x.valid_passno(pass_no):
            return x.apology('Invalid passport.', 'profile.new_visa_request')

        # Pasaport verilerini değişkene al
        pass_data = DataBase.execute('SELECT * FROM passports WHERE user_id = ? AND pass_no = ?', session['user_id'], pass_no)
        if not pass_data or not len(pass_data) == 1:
            x.apology('Passport data could not found.', 'profile_new_visa_request')

        # İstenilen ülkeyi formdan al
        country = request.form.get('country')
        if not country or not x.valid_country(country):
            return x.apology('Invalid country.', 'profile.new_visa_request')
        
        # Bu pasaportun bu ülkeye halihazırda mevcut başvurusu var mı kontrol et
        is_exist_request = DataBase.execute('SELECT * FROM visa_requests WHERE pass_id = ? AND country = ?', pass_data[0]['id'], country)
        if is_exist_request:
            return x.apology('There is already a pending request for this passport name.', 'profile.new_visa_request')

        # Tercih edilen tarihi formdan al
        pref_date = request.form.get('pref_date')
        if not pref_date or not x.valid_date(pref_date) or not x.valid_prefdate(pref_date):
            return x.apology('Invalid date. The earliest possible date can be two weeks later.', 'profile.new_visa_request')
        
        # Vize başvurusunu kaydet (try-except)
        try:
            # Kaydedecek olan sorguyu yaz
            DataBase.execute('INSERT INTO requests (user_id, pass_id, country, visa_type, prefferred_appointment_date) VALUES(?, ?, ?, ?, ?)', session['user_id'], pass_data[0]['id'], country.upper(), x.visatype(pass_data[0]['birth'], x.valid_date(pref_date)))
            return x.apology('Your request has been successfully created.', 'profile.requests')
        
        except ValueError:
            return x.apology('An error occurred. Please try again.', 'profile.new_visa_request')

        pass

    else:
        # Kullanıcının pasaportlarını sorgula
        passports = DataBase.execute('SELECT * FROM passports WHERE user_id = ?', session['user_id'])
        if not passports:
            return x.apology('You need to add a passport before you can create a new application.', 'profile.add_passport')
        
        return render_template('new.visa_request.html', passports = passports)
        


# Vize randevu talebi düzenleme route'unu ayarla
@profilebp.route('requests/visa/modify', methods=['GET', 'POST'])
@x.login_required
def modify_visa_request():
    if request.method == 'POST':
        # Başvuru numarasını args'dan al
        visa_request_id = request.args.get('id')
        if not visa_request_id or not visa_request_id.isdigit():
            return redirect(url_for('profile.requests'))
        # Args yoksa ya da numara değilse redirect yap

        # Başvuruyu başvuru id'siyle ve kullanıcı adıyla başvuruyu sorgula
        visa_request = DataBase.execute('SELECT * FROM requests WHERE id = ? AND user_id = ?', visa_request_id, session['user_id'])
        if not visa_request or not len(visa_request) == 1:
            return x.apology('Unauthorized access.', 'profile.requests')

        # Talep beklemede değilse hata ver (status != 0)
        if visa_request[0]['status'] != 0:
            return x.apology('Changes cannot be made because your appointment has already been created.', 'profile.requests')

        # Pasaport bilgisini formdan al
        pass_id = request.form.get('pass_id')
        if not pass_id or not pass_id.isdigit():
            return x.apology('Invalid passport.', 'profile.modify_visa_request', id = visa_request_id)
        
        # Pasaport yoksa hata ver
        pass_data = DataBase.execute('SELECT * FROM passports WHERE id = ? AND user_id = ?', pass_id, session['user_id'])
        if not pass_data or not len(pass_data) == 1:
            return x.apology('There is no passport associated with this number.', 'profile.modify')
        # Pasaport id değişmişse pasaportun halihazırda başvurusu olup olmadığını kontrol et
        
        # Ülkeyi formdan al
        # Ülke yoksa ya da geçersizse hata ver

        # Tercih edilen tarihi formdan al
        # Tarih yoksa ya da geçersizse hata ver

        # Bilgileri güncelle (try-except)
            # Güncelleme sorgusu yaz sadece gelen verileri güncelle
            
            # Hata mesajı ver ve talepler sayfasına yönlendir
        pass
    
    else:
        # Args ile başvuru numarasını al
        # Args yoksa ya da numara değilse redirect yap

        # Başvuruyu sorgula
        # Yoksa hata ver

        # Kullanıcının mevcut başvurudaki pasaportu haricindeki pasaportlarını sorgula
        # Pasaport yoksa hata ver

        # Başvuruyu ve pasaportları html'e gönder
        pass


# Vize randevu talebi iptal etme route'unu ayarla
@profilebp.route('requests/visa/cancel', methods=['GET', 'POST'])
@x.login_required
def cancellation_visa_request():
    if request.method == 'POST':
        # Talep id'sini al
        # Yoksa yada pozitif tam sayı değilse hata ver

        # Talebi sorgula
        # Talep status 0 değilse hata ver

        # Kullanıcı bilgilerini sorgula
        # Yoksa hata ver ve logout yap

        # Parolayı formdan al
        # Parola yoksa ya da eşleşmiyorsa hata ver

        # Talebi sil (try-except)
            # Silme sorgusunu yaz
            # Başarılı mesajı ver ve requests'e yönlendir

            # Hata, sonra dene mesajı döndür, requests sayfasına yönlendir
        pass

    else:
        # Talep id'sini al
        # Yoksa ya da pozitif tam sayı değilse hata ver

        # Kullanıcının bu id'ye sahip talebini sorgula
        # Yoksa ya da 1'den farklıysa hata ver
        
        # Talep bilgilerini html'e gönder
        pass


# Yeşil sigorta talebi oluşturma route'unu ayarla
@profilebp.route('/requests/greendcard/new', methods=['GET', 'POST'])
@x.login_required
def new_greencard_request():
    if request.method == 'POST':
        pass
    
    else:
        pass


# Yeşil sigorta talebi düzenleme route'unu ayarla
@profilebp.route('/requests/greencard/modify', methods=['GET', 'POST'])
@x.login_required
def modify_greencard_request():
    if request.method == 'POST':
        pass

    else:
        pass


# Yeşil sigorta talebi iptal etme route'unu ayarla
@profilebp.route('/requests/greencard/cancel', methods=['GET', 'POST'])
@x.login_required
def cancellation_greencard_request():
    if request.method == 'POST':
        pass

    else:
        pass