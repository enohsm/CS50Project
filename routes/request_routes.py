from .imports import *


# ENG: Assign variable for blueprint of visa routes
# TR: Vize rotalarını modülleyecek bir değişken ata
requestbp = Blueprint("request", __name__, url_prefix="/me/requests")


# ENG: Set up requests route
# TR: Requests routeunu ayarla
@requestbp.route("/")
@x.login_required
def requests():
    # ENG: Query last 5 visa requests of the user (ordered by request_time DESC)
    # TR: Kullanıcının son 5 adet vize başvuru taleplerini sorgula (request_time DESC)
    visa_requests = DataBase.execute(x.file_query('visa_requests_limited.sql'), session['user_id'])
    count_visa = len(visa_requests)

    # ENG: Query last 5 green card requests of the user (ordered by request_time DESC)
    # TR: Kullanıcının son 5 adet yeşil sigorta taleplerini sorgula (request_time DESC)
    gc_requests = DataBase.execute(x.file_query('gc_requests_limited.sql'), session['user_id'])
    count_gc = len(gc_requests)

    return render_template("my_requests.html", visa = visa_requests, greencard = gc_requests, count_visa = count_visa, count_gc = count_gc)


# ENG: Set up visa requests route
# TR: Visa requests route'unu ayarla
@requestbp.route('/visa')
@x.login_required
def visa_requests():
    # ENG: Query all visa requests of the user
    # TR: Kullanıcının tüm vize taleplerini sorgula
    visa_requests = DataBase.execute(x.file_query('visa_requests.sql'), session['user_id'])
    if not visa_requests:
        return x.apology('You do not have any visa requests.', 'request.new_visa_request')
    
    # ENG: Format all visa request dates as DD/MM/YYYY
    # TR: Tüm vize taleplerinin tarihlerini DD/MM/YYYY olarak formatla
    for request in visa_requests:
        request['request_date'] = datetime.strptime(request['request_date'], '%Y-%m-%d %H:%M:%S').strftime('%d/%m/%Y - %H:%M:%S')
    
    return render_template('my_visa_requests.html', visa_requests = visa_requests)


# ENG: Set up new visa appointment request route
# TR: Vize randevu talebi oluşturma route'unu ayarla
@requestbp.route('/visa/new', methods=['GET', 'POST'])
@x.login_required
def new_visa_request():
    if request.method == 'POST':
        # ENG: Get passport number from form
        # TR: Pasaport numarasını formdan al
        pass_no = request.form.get('pass_no')
        if not pass_no or not x.valid_passno(pass_no):
            return x.apology('Invalid passport.', 'request.new_visa_request')
        
        # ENG: Fetch passport data into variable
        # TR: Pasaport verilerini değişkene al
        pass_data = DataBase.execute('SELECT * FROM passports WHERE user_id = ? AND pass_no = ?', session['user_id'], pass_no)
        if not pass_data or not len(pass_data) == 1:
            return x.apology('Passport data could not found.', 'request.new_visa_request')

        # ENG: If passport is unconfirmed, raise error
        # TR: Pasaport onaylanmamışsa hata ver
        if pass_data[0]['confirmed'] == 0:
            return x.apology('You cannot create request with unconfirmed passport.', 'request.new_visa_request')

        # ENG: Get requested country from form
        # TR: İstenilen ülkeyi formdan al
        country = request.form.get('country')
        if not country or not x.valid_country(country):
            return x.apology('Invalid country.', 'request.new_visa_request')
        
        # ENG: Check if user already has a request for this country (status != 3 / Resulted application /)
        # TR: Bu kullanıcının bu ülkeye halihazırda mevcut başvurusu var mı kontrol et (status = 3 / Sonuçlanmış başvuru /)
        is_exist_request = DataBase.execute('SELECT * FROM visa_requests WHERE user_id = ? AND country = ? AND status != 3', session['user_id'], country)
        if is_exist_request:
            return x.apology('There is already a pending request for this passport.', 'request.new_visa_request')

        # ENG: Get preferred date from form
        # TR: Tercih edilen tarihi formdan al
        pref_date = request.form.get('pref_date')
        if not pref_date or not x.valid_date(pref_date) or not x.valid_prefdate(pref_date):
            return x.apology('Invalid date. The earliest possible date can be two weeks later.', 'request.new_visa_request')
        
        # ENG: Save visa request
        # TR: Vize başvurusunu kaydet
        try:

            # ENG: Write the query to insert data
            # Kaydedecek olan sorguyu yaz
            DataBase.execute('INSERT INTO visa_requests (user_id, pass_id, country, visa_type, prefferred_appointment_date) VALUES(?, ?, ?, ?, ?)', session['user_id'], pass_data[0]['id'], country.upper(), x.visatype(pass_data[0]['birth']), x.valid_date(pref_date))
            return x.apology('Your request has been successfully created.', 'request.visa_requests')
        
        except ValueError:
            return x.apology('An error occurred. Please try again.', 'request.new_visa_request')

    else:
        # ENG: Query user's passports
        # TR: Kullanıcının pasaportlarını sorgula
        passports = DataBase.execute('SELECT * FROM passports WHERE user_id = ? AND confirmed = 1', session['user_id'])
        if not passports:
            return x.apology('There is no passport available for which you can create a request. Please add a new passport.', 'profile.add_passport')

        # ENG: Create list for select options in form
        # TR: Formdaki "select" etiketine "options" ekleyebilmek adına liste oluştur
        countries = ['BULGARIA', 'GREECE', 'GERMANY', 'NETHERLANDS', 'AUSTRIA', 'ITALY']
        
        return render_template('new_visa_request.html', passports = passports, countries = countries)
        

# ENG: Set up modify visa request route
# TR: Vize randevu talebi düzenleme route'unu ayarla
@requestbp.route('/visa/modify', methods=['GET', 'POST'])
@x.login_required
def modify_visa_request():
    if request.method == 'POST':

        # ENG: Get visa request ID from args
        # TR: Başvuru numarasını args'dan al
        visa_request_id = request.args.get('id')
        if not visa_request_id or not visa_request_id.isdigit():
            return redirect(url_for('request.visa_requests'))

        # ENG: Query the request by ID and user
        # TR: Başvuruyu başvuru id'siyle ve kullanıcı adıyla başvuruyu sorgula
        visa_request = DataBase.execute('SELECT * FROM visa_requests WHERE id = ? AND user_id = ?', visa_request_id, session['user_id'])
        if not visa_request or not len(visa_request) == 1:
            return x.apology('Unauthorized access.', 'request.visa_requests')

        # ENG: If request is not pending, raise error (status != 0)
        # TR: Talep beklemede değilse hata ver (status != 0)
        if visa_request[0]['status'] != 0:
            return x.apology('Changes cannot be made because your appointment has already been created.', 'request.visa_requests')
        
        # ENG: Get country from form
        # TR: Ülkeyi formdan al
        country = request.form.get('country')
        if not country or not x.valid_country(country):
            return x.apology('Invalid country.', 'request.modify_visa_request', id = visa_request_id)
        
        # ENG: If country changed, check for another active request for this country
        # TR: Ülke değişmişse kullanıcının bu ülkeye aktif olan başka başvurusu var mı kontrol et
        if country != visa_request[0]['country']:
            is_exist_country_request = DataBase.execute('SELECT * FROM visa_requests WHERE user_id = ? AND id != ? AND country = ? AND status != ?', session['user_id'], visa_request_id, country, '2')
            if is_exist_country_request:
                return x.apology('You already have an active application for this country.', 'request.modify_visa_request', id = visa_request_id)
        
        # ENG: Get preferred date from form
        # TR: Tercih edilen tarihi formdan al
        pref_date = request.form.get('pref_date')
        if not pref_date or not x.valid_date(pref_date) or not x.valid_prefdate(pref_date):
            return x.apology('Invalid preffered date.', 'request.modify_visa_request', id = visa_request_id)

        # ENG: Update request information
        # TR: Bilgileri güncelle
        try:

            # ENG: Execute update query with new values only
            # TR: Güncelleme sorgusu yaz sadece gelen verileri güncelle
            DataBase.execute('UPDATE visa_requests SET country = ?, prefferred_appointment_date = ? WHERE id = ?', country, x.valid_date(pref_date), visa_request_id)
            return x.apology('Your request has been successfully modified.', 'request.visa_requests')

        # ENG: Handle error and redirect with message
        # TR: Hata yakalanırsa hata mesajı ver ve talepler sayfasına yönlendir
        except ValueError:
            return x.apology('An error occurred.', 'request.visa_requests')
    
    else:
        # ENG: Get request ID from args
        # TR: Args ile başvuru numarasını al
        request_id = request.args.get('id')
        if not request_id or not request_id.isdigit():
            return redirect('request.visa_requests')

        # ENG: Query user's request
        # TR: Kullanıcıya ait başvuruyu sorgula
        request_q = DataBase.execute('SELECT * FROM visa_requests WHERE id = ? AND user_id = ?', request_id, session['user_id'])
        if not request_q or len(request_q) != 1:
            return x.apology('Unauthorized access.', 'request.visa_requests')
        
        # ENG: If request is not pending, raise error
        # TR: Talep beklemede değilse hata ver
        if request_q[0]['status'] != 0:
            return x.apology('Changes cannot be made because your appointment has already been created.', 'request.visa_requests')
        
        # ENG: Format preferred date for form
        # TR: Başvurunun tercih edilen tarihini forma uygun şekilde biçimlendir
        request_q[0]['prefferred_appointment_date'] = datetime.strptime(request_q[0]['prefferred_appointment_date'], '%d/%m/%Y').strftime('%Y-%m-%d')
        
        # ENG: Check if passport used in this request still exists
        # TR: Kullanıcının bu başvuruda kullanılmış pasaportu hala mevcut mu kontrol et
        passport = DataBase.execute('SELECT pass_no, pass_exp FROM passports WHERE id = ?', request_q[0]['pass_id'])
        if not passport:
            return x.apology('Your passport could not found.', 'request.visa_requests')

        # ENG: Send request and passport info to HTML
        # TR: Başvuruyu ve pasaportları html'e gönder
        return render_template('modify_visa_request.html', requ = request_q[0], passport = passport[0], countries = sorted(x.countries()))


# ENG: Set up cancellation of visa request route
# TR: Vize randevu talebi iptal etme route'unu ayarla
@requestbp.route('/visa/cancel', methods=['GET', 'POST'])
@x.login_required
def cancellation_visa_request():
    if request.method == 'POST':
        # ENG: Get request ID
        # TR: Talep id'sini al
        request_id = request.args.get('id')
        if not request_id or not request_id.isdigit():
            return redirect(url_for('request.visa_requests'))

        # ENG: Query user's request
        # TR: Kullanıcının bu talebini sorgula
        visa_request = DataBase.execute('SELECT * FROM visa_requests WHERE id = ? AND user_id = ?', request_id, session['user_id'])
        if not visa_request or len(visa_request) != 1:
            return x.apology('Unauthorized access.', 'request.visa_requests')
        
        # ENG: If status is not 0, cannot cancel
        # TR: Talep status 0 değilse hata ver (talep işleme girmişse hata)
        if visa_request[0]['status'] != 0:
            return x.apology('Cancellation not available after appointment creation.', 'request.visa_requests')

        # ENG: Get user data
        # TR: Kullanıcı bilgilerini sorgula
        user_data = DataBase.execute('SELECT * FROM users WHERE id = ?', session['user_id'])
        if not user_data:
            return x.apology('An error occurred. Please re-login.', 'main.logout')

        # ENG: Get password from form and check match
        # TR: Parolayı formdan al ve eşleşmeyi kontrol et
        password = request.form.get('password')
        if not password or not check_password_hash(user_data[0]['password'], password):
            return x.apology('Invalid password.', 'request.cancellation_visa_request', id = request_id)

        # ENG: Delete request
        # TR: Talebi sil
        try:

            # ENG: Execute delete query
            # TR: Silme sorgusunu yaz
            DataBase.execute('DELETE FROM visa_requests WHERE id = ? AND user_id = ?', request_id, session['user_id'])
            return x.apology('Your request has been successfully cancelled.', 'request.visa_requests')

        except ValueError:
            # ENG: Handle error and redirect
            # TR: Hata, sonra dene mesajı döndür, requests sayfasına yönlendir
            return x.apology('An error occurred. Please try again.', 'request.visa_requests')

    else:
        # ENG: Get request ID from args
        # TR: Talep id'sini al
        req_id = request.args.get('id')
        if not req_id or not req_id.isdigit():
            return redirect(url_for('request.visa_requests'))

        # ENG: Get request ID from args
        # TR: Kullanıcının bu id'ye sahip talebini sorgula
        request_check = DataBase.execute('SELECT * FROM visa_requests WHERE id = ? AND user_id = ?', req_id, session['user_id'])
        if not request_check or len(request_check) != 1:
            return x.apology('Unauthorized access.', 'request.visa_requests')
        
        # ENG: If request is already processed, cannot cancel
        # TR: Talep işleme girmişse yönlendir
        if request_check[0]['status'] != 0:
            return x.apology('Cancellation not available after appointment creation.', 'request.visa_requests')

        # ENG: Send request info to HTML
        # TR: Talep bilgilerini html'e gönder
        return render_template('cancel_visa_request.html', requ = request_check[0])


# ENG: Set up green card requests route
# TR: Yeşil sigorta talepleri route'unu ayarla
@requestbp.route('/greencard', methods=['GET', 'POST'])
@x.login_required
def gc_requests():
    # ENG: Query user's green card requests
    # TR: Kullanıcının yeşil sigorta taleplerini sorgula
    greencards = DataBase.execute(x.file_query('gc_requests.sql'), session['user_id'])

    # ENG: Format dates if requests exist
    # TR: Eğer talep mevcut ise tarihlerini formatla
    if greencards:
        for greencard in greencards:
            greencard['request_date'] = datetime.strptime(greencard['request_date'], '%Y-%m-%d %H:%M:%S').strftime('%d/%m/%Y - %H:%M:%S')

    return render_template('my_gc_requests.html', greencards = greencards)

# ENG: Set up new green card request route
# TR: Yeşil sigorta talebi oluşturma route'unu ayarla
@requestbp.route('/greendcard/new', methods=['GET', 'POST'])
@x.login_required
def new_gc_request():
    if request.method == 'POST':
        # ENG: Get vehicle ID from form
        # TR: Araç id'sini formdan al
        vehicle_id = request.form.get('vehicle')
        if not vehicle_id or not vehicle_id.isdigit():
            return x.apology('Invalid vehicle.', 'request.new_gc_request')

        # ENG: Check if user owns this vehicle
        # TR: Kullanıcının bu araca sahip olup olmadığını kontrol et
        vehicle = DataBase.execute('SELECT * FROM vehicles WHERE id = ? AND user_id = ?', vehicle_id, session['user_id'])
        if not vehicle or len(vehicle) != 1:
            return x.apology('You are not owner of this vehicle.', 'request.new_gc_request')
        
        # ENG: Check if there is already an active request for this vehicle
        # TR: Bu araca dair aktif olan talep olup olmadığını kontrol et
        existing_request = DataBase.execute('SELECT * FROM gc_requests WHERE vehicle_id = ? AND status != 2', vehicle_id)
        if existing_request:
            return x.apology('You have already an active request for this vehicle.', 'request.new_gc_request')
        
        # ENG: Get start date from form
        # TR: Sigorta başlangıç tarihini formdan al
        start_date = request.form.get('start_date')
        if not start_date or not x.valid_startdate(start_date):
            return x.apology('Invalid start date.', 'request.new_gc_request')
        
        # ENG: Get coverage period from form
        # TR: Kapsam süresini formdan al
        cov_period = request.form.get('cov_period')
        if not cov_period or cov_period not in ['3M', '1M', '15D']:
            return x.apology('Invalid period.', 'request.new_gc_request')
        
        # ENG: Save to system
        # TR: Sisteme kaydet
        try:
            DataBase.execute('INSERT INTO gc_requests (user_id, vehicle_id, start_date, cov_period) VALUES(?, ?, ?, ?)', session['user_id'], vehicle_id, x.valid_date(start_date), cov_period.upper())
            return x.apology('Your green card insurance request has been successfully registered.', 'request.gc_requests')

        except ValueError:
            return x.apology('An error occurred. Please try again.', 'request.gc_requests')

    else:
        # ENG: Check if user has vehicles
        # TR: Kullanıcının aracı olup olmadığını kontrol et
        vehicles = DataBase.execute('SELECT * FROM vehicles WHERE user_id = ?', session['user_id'])
        if not vehicles:
            return x.apology('You have no vehicle to create request for green card insurance.', 'profile.add_vehicle')

        return render_template('new_greencard_request.html', vehicles = vehicles)


# ENG: Set up modify green card request route
# TR: Yeşil sigorta talebi düzenleme route'unu ayarla
@requestbp.route('/greencard/modify', methods=['GET', 'POST'])
@x.login_required
def modify_gc_request():
    if request.method == 'POST':
        request_id = request.args.get('id')
        if not request_id or not request_id.isdigit():
            return redirect(url_for('request.gc_requests'))
        
        # ENG: Check if user owns this request and status is pending
        # TR: Kullanıcı bu talebe sahip mi kontrol et? (!! iyileştirme : status kontrolü veritabanı sorgusuyla yapılıyor !!)
        gc_request = DataBase.execute(x.file_query('active_gc_requests.sql'), request_id, session['user_id'])
        if not gc_request or len(gc_request) != 1:
            return x.apology('Unauthorized access or request status is not "Pending".', 'request.gc_requests')
        
        # ENG: Get data from form
        # TR: Verileri formdan al
        start_date = request.form.get('start_date')
        if not start_date or not x.valid_startdate(start_date):
            return x.apology('Invalid start date.', 'request.modify_gc_request', id = request_id)
        
        cov_period = request.form.get('cov_period')
        if not cov_period or cov_period not in ['3M', '1M', '15D']:
            return x.apology('Invalid period.', 'request.modify_gc_request', id = request_id)
        
        # ENG: Update request with new values
        # TR: Düzenlenmiş şekilde güncelle
        try:
            DataBase.execute('UPDATE gc_requests SET start_date = ?, cov_period = ? WHERE id = ? AND user_id = ?', x.valid_date(start_date), cov_period.upper(), request_id, session['user_id'])
            return x.apology('Your green card request has been successfully modified.', 'request.gc_requests')
        
        except ValueError:
            return x.apology('An error occurred. Please try again.', 'request.gc_requests')

    else:
        requ_id = request.args.get('id')
        if not requ_id or not requ_id.isdigit():
            return redirect(url_for('request.gc_requests'))
        
        # ENG: Check ownership of request
        # TR: Kullanıcı bu talebe sahip mi kontrol et
        gc_request = DataBase.execute(x.file_query('active_gc_requests.sql'), requ_id, session['user_id'])
        if not gc_request or len(gc_request) != 1:
            return x.apology('Unauthorized access or request is not active.', 'request.gc_requests')
        
        # ENG: Format date for form
        # TR: Tarihi fomrda gösterilebilecek şekilde formatla
        gc_request[0]['startdate'] = datetime.strptime(gc_request[0]['startdate'], '%d/%m/%Y').strftime('%Y-%m-%d')

        # ENG: Create list for select options in form
        # TR: Html içerisindeki "select" etiketinde "options" için liste oluştur
        periods = ['3M', '1M', '15D']

        return render_template('modify_greencard_request.html', greencard = gc_request[0], periods = periods)


# ENG: Set up cancellation of green card request route
# TR: Yeşil sigorta talebi iptal etme route'unu ayarla
@requestbp.route('/greencard/cancel', methods=['GET', 'POST'])
@x.login_required
def cancellation_gc_request():
    if request.method == 'POST':
        request_id = request.args.get('id')
        if not request_id or not request_id.isdigit():
            return redirect(url_for('request.gc_requests'))
        
        # ENG: Check if user has pending green card request with this ID
        # TR: Kullanıcının bu ID'ye sahip, bekleyen yeşil sigorta başvurusu var mı?
        greencard = DataBase.execute(x.file_query('active_gc_requests.sql'), request_id, session['user_id'])
        if not greencard or len(greencard) != 1:
            return x.apology('Unauthorized access or request status is not "Pending".', 'request.gc_requests')
        
        # ENG: Get user password from database
        # TR: Kullanıcı bilgilerini veritabanından al
        user_data = DataBase.execute('SELECT password FROM users WHERE id = ?', session['user_id'])
        if not user_data or len(user_data) != 1:
            return x.apology('An error occurred, please re-login.', 'profile.logout')
        
        # ENG: Store password in variable
        # TR: Şifreyi bir değişkene al
        cur_password = user_data[0]['password']

        # ENG: Get password from form and check match
        # TR: Formdan şifreyi al ve eşleşmeyi kontrol et
        password = request.form.get('password')
        if not password or not check_password_hash(cur_password, password):
            return x.apology('Invalid password.', 'request.cancellation_gc_request', id = request_id)
        
        # ENG: Delete the request
        # TR: Talebi sil
        try:
            DataBase.execute('DELETE FROM gc_requests WHERE id = ? AND user_id = ?', request_id, session['user_id'])
            return x.apology('Your request has been successfully cancelled.', 'request.gc_requests')
        
        except ValueError:
            return x.apology('An error occurred, please try again.', 'request.gc_requests')

    else:
        requ_id = request.args.get('id')
        if not requ_id or not requ_id.isdigit():
            return redirect(url_for('request.gc_requests'))
        
        # ENG: Query pending green card request of user
        # TR: Kullanıcının beklemede olan talebini sorgula
        greencard = DataBase.execute(x.file_query('active_gc_requests.sql'), requ_id, session['user_id'])
        if not greencard or len(greencard) != 1:
            return x.apology('Unauthorized access or request is not active.', 'request.gc_requests')
        
        return render_template('cancel_greencard_request.html', greencard = greencard[0])