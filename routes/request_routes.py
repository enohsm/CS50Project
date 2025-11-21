from .imports import *


# ENG: Assign variable for blueprint of visa routes
# TR: Vize rotalarını modülleyecek bir değişken ata
requestbp = Blueprint("request", __name__, url_prefix="/me/requests")


# Requests routeunu ayarla
@requestbp.route("/")
@x.login_required
def requests():
    # Kullanıcının son 5 adet vize başvuru taleplerini sorgula (request_time DESC)
    visa_requests = DataBase.execute(x.file_query('visa_requests_limited.sql'), session['user_id'])
    count_visa = len(visa_requests)

    # Kullanıcının son 5 adet yeşil sigorta taleplerini sorgula (request_time DESC)
    gc_requests = DataBase.execute(x.file_query('gc_requests_limited.sql'), session['user_id'])
    count_gc = len(gc_requests)

    return render_template("my_requests.html", visa = visa_requests, greencard = gc_requests, count_visa = count_visa, count_gc = count_gc)


# Visa requests route'unu ayarla
@requestbp.route('/visa')
@x.login_required
def visa_requests():
    # Kullanıcının tüm vize taleplerini sorgula
    visa_requests = DataBase.execute(x.file_query('visa_requests.sql'), session['user_id'])
    if not visa_requests:
        return x.apology('You do not have any visa requests.', 'request.new_visa_request')
    for request in visa_requests:
        request['request_date'] = datetime.strptime(request['request_date'], '%Y-%m-%d %H:%M:%S').strftime('%d/%m/%Y - %H:%M:%S')
    
    return render_template('my_visa_requests.html', visa_requests = visa_requests)


# Vize randevu talebi oluşturma route'unu ayarla
@requestbp.route('/visa/new', methods=['GET', 'POST'])
@x.login_required
def new_visa_request():
    if request.method == 'POST':
        # Pasaport numarasını formdan al
        pass_no = request.form.get('pass_no')
        if not pass_no or not x.valid_passno(pass_no):
            return x.apology('Invalid passport.', 'request.new_visa_request')

        # Pasaport verilerini değişkene al
        pass_data = DataBase.execute('SELECT * FROM passports WHERE user_id = ? AND pass_no = ?', session['user_id'], pass_no)
        if not pass_data or not len(pass_data) == 1:
            return x.apology('Passport data could not found.', 'request.new_visa_request')

        # Pasaport onaylanmamışsa hata ver
        if pass_data[0]['confirmed'] == 0:
            return x.apology('You cannot create request with unconfirmed passport.', 'request.new_visa_request')

        # İstenilen ülkeyi formdan al
        country = request.form.get('country')
        if not country or not x.valid_country(country):
            return x.apology('Invalid country.', 'request.new_visa_request')
        
        # Bu kullanıcının bu ülkeye halihazırda mevcut başvurusu var mı kontrol et (status = 3 / Sonuçlanmış başvuru /)
        is_exist_request = DataBase.execute('SELECT * FROM visa_requests WHERE user_id = ? AND country = ? AND status != 3', session['user_id'], country)
        if is_exist_request:
            return x.apology('There is already a pending request for this passport.', 'request.new_visa_request')

        # Tercih edilen tarihi formdan al
        pref_date = request.form.get('pref_date')
        if not pref_date or not x.valid_date(pref_date) or not x.valid_prefdate(pref_date):
            return x.apology('Invalid date. The earliest possible date can be two weeks later.', 'request.new_visa_request')
        
        # Vize başvurusunu kaydet (try-except)
        try:
            # Kaydedecek olan sorguyu yaz
            DataBase.execute('INSERT INTO visa_requests (user_id, pass_id, country, visa_type, prefferred_appointment_date) VALUES(?, ?, ?, ?, ?)', session['user_id'], pass_data[0]['id'], country.upper(), x.visatype(pass_data[0]['birth']), x.valid_date(pref_date))
            return x.apology('Your request has been successfully created.', 'request.visa_requests')
        
        except ValueError:
            return x.apology('An error occurred. Please try again.', 'request.new_visa_request')

    else:
        # Kullanıcının pasaportlarını sorgula
        passports = DataBase.execute('SELECT * FROM passports WHERE user_id = ? AND confirmed = 1', session['user_id'])
        if not passports:
            return x.apology('There is no passport available for which you can create a request. Please add a new passport.', 'profile.add_passport')

        countries = ['BULGARIA', 'GREECE', 'GERMANY', 'NETHERLANDS', 'AUSTRIA', 'ITALY']
        
        return render_template('new_visa_request.html', passports = passports, countries = countries)
        

# Vize randevu talebi düzenleme route'unu ayarla
@requestbp.route('/visa/modify', methods=['GET', 'POST'])
@x.login_required
def modify_visa_request():
    if request.method == 'POST':
        # Başvuru numarasını args'dan al
        visa_request_id = request.args.get('id')
        if not visa_request_id or not visa_request_id.isdigit():
            return redirect(url_for('request.visa_requests'))

        # Başvuruyu başvuru id'siyle ve kullanıcı adıyla başvuruyu sorgula
        visa_request = DataBase.execute('SELECT * FROM visa_requests WHERE id = ? AND user_id = ?', visa_request_id, session['user_id'])
        if not visa_request or not len(visa_request) == 1:
            return x.apology('Unauthorized access.', 'request.visa_requests')

        # Talep beklemede değilse hata ver (status != 0)
        if visa_request[0]['status'] != 0:
            return x.apology('Changes cannot be made because your appointment has already been created.', 'request.visa_requests')
        
        # Ülkeyi formdan al
        country = request.form.get('country')
        if not country or not x.valid_country(country):
            return x.apology('Invalid country.', 'request.modify_visa_request', id = visa_request_id)
        
        # Ülke değişmişse kullanıcının bu ülkeye aktif olan başka başvurusu var mı kontrol et
        if country != visa_request[0]['country']:
            is_exist_country_request = DataBase.execute('SELECT * FROM visa_requests WHERE user_id = ? AND id != ? AND country = ? AND status != ?', session['user_id'], visa_request_id, country, '2')
            if is_exist_country_request:
                return x.apology('You already have an active application for this country.', 'request.modify_visa_request', id = visa_request_id)

        # Tercih edilen tarihi formdan al
        pref_date = request.form.get('pref_date')
        if not pref_date or not x.valid_date(pref_date) or not x.valid_prefdate(pref_date):
            return x.apology('Invalid preffered date.', 'request.modify_visa_request', id = visa_request_id)

        # Bilgileri güncelle (try-except)
        try:
            # Güncelleme sorgusu yaz sadece gelen verileri güncelle
            DataBase.execute('UPDATE visa_requests SET country = ?, prefferred_appointment_date = ? WHERE id = ?', country, x.valid_date(pref_date), visa_request_id)
            return x.apology('Your request has been successfully modified.', 'request.visa_requests')

        # Hata yakalanırsa hata mesajı ver ve talepler sayfasına yönlendir
        except ValueError:
            return x.apology('An error occurred.', 'request.visa_requests')
    
    else:
        # Args ile başvuru numarasını al
        request_id = request.args.get('id')
        if not request_id or not request_id.isdigit():
            return redirect('request.visa_requests')

        # Başvuruyu sorgula
        request_q = DataBase.execute('SELECT * FROM visa_requests WHERE id = ? AND user_id = ?', request_id, session['user_id'])
        if not request_q or len(request_q) != 1:
            return x.apology('Unauthorized access.', 'request.visa_requests')
        
        # Talep beklemede değilse hata ver
        if request_q[0]['status'] != 0:
            return x.apology('Changes cannot be made because your appointment has already been created.', 'request.visa_requests')
        
        request_q[0]['prefferred_appointment_date'] = datetime.strptime(request_q[0]['prefferred_appointment_date'], '%d/%m/%Y').strftime('%Y-%m-%d')
        print(request_q[0]['prefferred_appointment_date'])
        passport = DataBase.execute('SELECT pass_no, pass_exp FROM passports WHERE id = ?', request_q[0]['pass_id'])
        if not passport:
            return x.apology('Your passport could not found.', 'request.visa_requests')

        # Başvuruyu ve pasaportları html'e gönder
        return render_template('modify_visa_request.html', requ = request_q[0], passport = passport[0], countries = sorted(x.countries()))


# Vize randevu talebi iptal etme route'unu ayarla
@requestbp.route('/visa/cancel', methods=['GET', 'POST'])
@x.login_required
def cancellation_visa_request():
    if request.method == 'POST':
        # Talep id'sini al
        request_id = request.args.get('id')
        if not request_id or not request_id.isdigit():
            return redirect(url_for('request.visa_requests'))

        # Talebi sorgula
        visa_request = DataBase.execute('SELECT * FROM visa_requests WHERE id = ? AND user_id = ?', request_id, session['user_id'])
        if not visa_request or len(visa_request) != 1:
            return x.apology('Unauthorized access.', 'request.visa_requests')
        
        # Talep status 0 değilse hata ver
        if visa_request[0]['status'] != 0:
            return x.apology('Cancellation not available after appointment creation.', 'request.visa_requests')

        # Kullanıcı bilgilerini sorgula
        user_data = DataBase.execute('SELECT * FROM users WHERE id = ?', session['user_id'])
        if not user_data:
            return x.apology('An error occurred. Please re-login.', 'main.logout')

        # Parolayı formdan al
        password = request.form.get('password')
        if not password or not check_password_hash(user_data[0]['password'], password):
            return x.apology('Invalid password.', 'request.cancellation_visa_request', id = request_id)

        # Talebi sil (try-except)
        try:
            # Silme sorgusunu yaz
            DataBase.execute('DELETE FROM visa_requests WHERE id = ? AND user_id = ?', request_id, session['user_id'])
            return x.apology('Your request has been successfully cancelled.', 'request.visa_requests')

        except ValueError:
            # Hata, sonra dene mesajı döndür, requests sayfasına yönlendir
            return x.apology('An error occurred. Please try again.', 'request.visa_requests')

    else:
        # Talep id'sini al
        req_id = request.args.get('id')
        if not req_id or not req_id.isdigit():
            return redirect(url_for('request.visa_requests'))

        # Kullanıcının bu id'ye sahip talebini sorgula
        request_check = DataBase.execute('SELECT * FROM visa_requests WHERE id = ? AND user_id = ?', req_id, session['user_id'])
        if not request_check or len(request_check) != 1:
            return x.apology('Unauthorized access.', 'request.visa_requests')
        
        if request_check[0]['status'] != 0:
            return x.apology('Cancellation not available after appointment creation.', 'request.visa_requests')

        # Talep bilgilerini html'e gönder
        return render_template('cancel_visa_request.html', requ = request_check[0])


# Yeşil sigorta talepleri route'unu ayarla
@requestbp.route('/greencard', methods=['GET', 'POST'])
@x.login_required
def gc_requests():
    # Kullanıcının yeşil sigorta taleplerini sorgula
    greencards = DataBase.execute(x.file_query('gc_requests.sql'), session['user_id'])

    if greencards:
        for greencard in greencards:
            greencard['request_date'] = datetime.strptime(greencard['request_date'], '%Y-%m-%d %H:%M:%S').strftime('%d/%m/%Y - %H:%M:%S')

    return render_template('my_gc_requests.html', greencards = greencards)


# Yeşil sigorta talebi oluşturma route'unu ayarla
@requestbp.route('/greendcard/new', methods=['GET', 'POST'])
@x.login_required
def new_gc_request():
    if request.method == 'POST':
        # Araç id'sini formdan al
        vehicle_id = request.form.get('vehicle')
        if not vehicle_id or not vehicle_id.isdigit():
            return x.apology('Invalid vehicle.', 'request.new_gc_request')

        # Kullanıcının bu araca sahip olup olmadığını kontrol et
        vehicle = DataBase.execute('SELECT * FROM vehicles WHERE id = ? AND user_id = ?', vehicle_id, session['user_id'])
        if not vehicle or len(vehicle) != 1:
            return x.apology('You are not owner of this vehicle.', 'request.new_gc_request')
        
        # Bu araca dair status 0 olan talep olup olmadığını kontrol et
        existing_request = DataBase.execute('SELECT * FROM gc_requests WHERE vehicle_id = ? AND status = 0', vehicle_id)
        if existing_request:
            return x.apology('You have already an active request for this vehicle.', 'request.new_gc_request')

        # Sigorta başlangıç tarihini formdan al
        start_date = request.form.get('start_date')
        if not start_date or not x.valid_startdate(start_date):
            return x.apology('Invalid start date.', 'request.new_gc_request')
        
        # Kapsam süresini formdan al
        cov_period = request.form.get('cov_period')
        if not cov_period or cov_period not in ['3M', '1M', '15D']:
            return x.apology('Invalid period.', 'request.new_gc_request')
        
        # Sisteme try-except ile kaydet
        try:
            DataBase.execute('INSERT INTO gc_requests (user_id, vehicle_id, start_date, cov_period) VALUES(?, ?, ?, ?)', session['user_id'], vehicle_id, x.valid_date(start_date), cov_period.upper())
            return x.apology('Your green card insurance request has been successfully registered.', 'request.gc_requests')

        except ValueError:
            return x.apology('An error occurred. Please try again.', 'request.gc_requests')

    else:
        # Kullanıcının aracı olup olmadığını kontrol et
        vehicles = DataBase.execute('SELECT * FROM vehicles WHERE user_id = ?', session['user_id'])
        if not vehicles:
            return x.apology('You have no vehicle to create request for green card insurance.', 'profile.add_vehicle')

        return render_template('new_greencard_request.html', vehicles = vehicles)


# Yeşil sigorta talebi düzenleme route'unu ayarla
@requestbp.route('/greencard/modify', methods=['GET', 'POST'])
@x.login_required
def modify_gc_request():
    if request.method == 'POST':
        request_id = request.args.get('id')
        if not request_id or not request_id.isdigit():
            return redirect(url_for('request.gc_requests'))
        
        gc_request = DataBase.execute(x.file_query('active_gc_requests.sql'), request_id, session['user_id'])
        if not gc_request or len(gc_request) != 1:
            return x.apology('Unauthorized access or request status is not "Pending".', 'request.gc_requests')
        
        start_date = request.form.get('start_date')
        if not start_date or not x.valid_startdate(start_date):
            return x.apology('Invalid start date.', 'request.modify_gc_request', id = request_id)
        
        cov_period = request.form.get('cov_period')
        if not cov_period or cov_period not in ['3M', '1M', '15D']:
            return x.apology('Invalid period.', 'request.modify_gc_request', id = request_id)
        
        try:
            DataBase.execute('UPDATE gc_requests SET start_date = ?, cov_period = ? WHERE id = ? AND user_id = ?', x.valid_date(start_date), cov_period.upper(), request_id, session['user_id'])
            return x.apology('Your green card request has been successfully modified.', 'request.gc_requests')
        
        except ValueError:
            return x.apology('An error occurred. Please try again.', 'request.gc_requests')

    else:
        requ_id = request.args.get('id')
        if not requ_id or not requ_id.isdigit():
            return redirect(url_for('request.gc_requests'))
        
        gc_request = DataBase.execute(x.file_query('active_gc_requests.sql'), requ_id, session['user_id'])
        if not gc_request or len(gc_request) != 1:
            return x.apology('Unauthorized access or request is not active.', 'request.gc_requests')
        
        gc_request[0]['startdate'] = datetime.strptime(gc_request[0]['startdate'], '%d/%m/%Y').strftime('%Y-%m-%d')

        periods = ['3M', '1M', '15D']

        return render_template('modify_greencard_request.html', greencard = gc_request[0], periods = periods)


# Yeşil sigorta talebi iptal etme route'unu ayarla
@requestbp.route('/greencard/cancel', methods=['GET', 'POST'])
@x.login_required
def cancellation_gc_request():
    if request.method == 'POST':
        request_id = request.args.get('id')
        if not request_id or not request_id.isdigit():
            return redirect(url_for('request.gc_requests'))
        
        greencard = DataBase.execute(x.file_query('active_gc_requests.sql'), request_id, session['user_id'])
        if not greencard or len(greencard) != 1:
            return x.apology('Unauthorized acces or request status is not "Pending".', 'request.gc_requests')
        
        user_data = DataBase.execute('SELECT password FROM users WHERE id = ?', session['user_id'])
        if not user_data or len(user_data) != 1:
            return x.apology('An error occurred, please re-login.', 'profile.logout')
        
        cur_password = user_data[0]['password']

        password = request.form.get('password')
        if not password or not check_password_hash(cur_password, password):
            return x.apology('Invalid password.', 'request.cancellation_gc_request', id = request_id)
        
        try:
            DataBase.execute('DELETE FROM gc_requests WHERE id = ? AND user_id = ?', request_id, session['user_id'])
            return x.apology('Your request has been successfully cancelled.', 'request.gc_requests')
        
        except ValueError:
            return x.apology('An error occurred, please try again.', 'request.gc_requests')

    else:
        requ_id = request.args.get('id')
        if not requ_id or not requ_id.isdigit():
            return redirect(url_for('request.gc_requests'))
        
        greencard = DataBase.execute(x.file_query('active_gc_requests.sql'), requ_id, session['user_id'])
        if not greencard or len(greencard) != 1:
            return x.apology('Unauthorized access or request is not active.', 'request.gc_requests')
        
        return render_template('cancel_greencard_request.html', greencard = greencard[0])