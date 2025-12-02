from .imports import *

# ENG: Setting up the blueprint
# TR: Modülü ayarlıyorum
dbbp = Blueprint("dashboard", __name__, url_prefix="/dashboard")


# ENG: Employee dashboard (operation counts)
# TR: Çalışan arayüzü (işlem sayıları)
@dbbp.route('/')
@x.login_required('employee')
def employee_db():
    count_all_visa_requests = DataBase.execute('SELECT COUNT(*) AS count FROM visa_requests')

    count_all_greencard_requests = DataBase.execute('SELECT COUNT(*) AS count FROM gc_requests')

    count_unconfirmed_passports = DataBase.execute('SELECT COUNT(*) AS count FROM passports WHERE confirmed != 1')
    
    count_awaiting_visa_requests = DataBase.execute('SELECT COUNT(*) AS count FROM visa_requests WHERE status = 0')

    count_confirmed_visa_appointment = DataBase.execute('SELECT COUNT(*) AS count FROM visa_requests WHERE status = 1')

    count_awaiting_gc_requests = DataBase.execute('SELECT COUNT(*) AS count FROM gc_requests WHERE status = 0')

    count_applicated_visa_requests = DataBase.execute('SELECT COUNT(*) AS count FROM visa_requests WHERE status = 2')

    return render_template('employee_dashboard.html',
                           visas_all = count_all_visa_requests[0], 
                           passports = count_unconfirmed_passports[0],
                           waiting_visa = count_awaiting_visa_requests[0],
                           confirmed_visa = count_confirmed_visa_appointment[0],
                           waiting_gc = count_awaiting_gc_requests[0],
                           applicated_visa = count_applicated_visa_requests[0],
                           greencards_all = count_all_greencard_requests[0])


# ENG: Passports awaiting approval
# TR: Onay bekleyen pasaportlar
@dbbp.route('/confirmation')
@x.login_required('employee')
def passport_confirmation():
    passports = DataBase.execute('SELECT users.username, passports.id, passports.name, passports.surname, passports.pass_no, passports.sex, passports.birth, passports.pass_exp, passports.ident_no FROM passports JOIN users ON passports.user_id = users.id WHERE passports.confirmed = 0')
    
    return render_template('passport_confirmation.html', passports = passports)

# ENG: Approve passport
# TR: Pasaport onaylama
@dbbp.route('/confirmation/confirm', methods = ['GET', 'POST'])
@x.login_required('employee')
def confirm_passport():
    if request.method == 'POST':
        # ENG: Get passport ID from URL
        # TR: URL'den pasaport ID'sini al 
        pass_id = request.args.get('id')
        if not pass_id or not pass_id.isdigit():
            return redirect(url_for('dashboard.passport_confirmation'))
        
        # ENG: Check passport and approval status
        # TR: Pasaportu ve onayın durumunu kontrol et
        pass_data = DataBase.execute('SELECT * FROM passports WHERE id = ? AND confirmed = 0', pass_id)
        if not pass_data or len(pass_data) != 1:
            return x.apology('Passport could not found or already confirmed.', 'dashboard.passport_confirmation')
        
        # ENG: Approve passport (update in database)
        # TR: Pasaportu onayla (Veritabanında güncelle)
        try:
            DataBase.execute('UPDATE passports SET confirmed = 1 WHERE id = ?', pass_id)
            return x.apology(f'The passport with number {pass_data[0]['pass_no']} has been successfully approved.', 'dashboard.passport_confirmation')
        
        except ValueError:
            return x.apology('An error occurred. Please try again.', 'dashboard.passport_confirmation')
        
    else:
        return redirect(url_for('dashboard.passport_confirmation'))

# ENG: Cancel passport
# TR: Pasaport iptali
@dbbp.route('/confirmation/cancel', methods = ['GET', 'POST'])
@x.login_required('employee')
def cancel_passport():
    if request.method == 'POST':
        # ENG: Get passport ID
        # TR: Pasaport id sini al
        pass_id = request.args.get('id')
        if not pass_id or not pass_id.isdigit():
            return redirect(url_for('dashboard.passport_confirmation'))
        
        # ENG: Check passport and approval status
        # TR: Pasaportu ve onayın durumunu kontrol et
        pass_data = DataBase.execute('SELECT * FROM passports WHERE id = ? AND confirmed = 0', pass_id)
        if not pass_data or len(pass_data) != 1:
            return x.apology('Passport could not found or already confirmed.', 'dashboard.passport_confirmation')
        
        # ENG: Cancel passport (delete from database)
        # TR: Pasaportu iptal et (Veritabanından sil)
        try:
            DataBase.execute('DELETE FROM passports WHERE id = ?', pass_id)
            
            # ENG: Delete passport image
            # TR: Pasaport görüntüsünü sil
            if os.path.exists(f'static/passports/{pass_data[0]['img']}'):
                os.remove(f'static/passports/{pass_data[0]['img']}')
            return x.apology(f'The passport with number {pass_data[0]['pass_no']} has been successfully cancelled.', 'dashboard.passport_confirmation')

        except:
            return x.apology('An error occurred. Please try again.', 'dashboard.passport_confirmation')
        
    else:
        return redirect(url_for('dashboard.passport_confirmation'))
    

# ENG: Route for viewing all green card requests
# TR: Tüm yeşil sigorta taleplerini görüntüleme rotası
@dbbp.route('/greencard_requests_all')
@x.login_required('employee')
def all_greencards():
    gc_requests = DataBase.execute(x.file_query('all_gc_requests.sql'))
    return render_template('all_greencards.html', requests = gc_requests)

# ENG: Pending green card requests
# TR: Onay bekleyen yeşil sigorta talepleri
@dbbp.route('/greencard_requests')
@x.login_required('employee')
def pending_greencards():
    gc_requests = DataBase.execute(x.file_query('pending_gc_requests.sql'))

    return render_template('greencard_requests.html', greencards = gc_requests)

# ENG: Create green card order (mailorder)
# TR: Yeşil sigorta siparişini oluşturma (mailorder)
@dbbp.route('/greencard_requests/send', methods=['GET', 'POST'])
@x.login_required('employee')
def send_greencard():
    if request.method == 'POST':
        request_id = request.form.get('request_id')
        if not request_id or not request_id.isdigit():
            return redirect(url_for('dashboard.pending_greencards'))
        
        # ENG: Check if the request is still pending
        # TR: Talep hala mevcut mu kontrol et (Form beklerken bir başka çalışan siparişi oluşturmuş olabilir!)
        is_exist_request = DataBase.execute('SELECT * FROM gc_requests WHERE id = ? AND status = 0', request_id)
        if not is_exist_request:
            return x.apology('This request is not pending.', 'dashboard.pending_greencards')
        
        # ENG: Get data from form
        # TR: Verileri formdan al
        name_ = request.form.get('name')
        if not name_:
            return x.apology('You must enter a name.', 'dashboard.send_greencard', id = request_id)
        
        address_ = request.form.get('address')
        if not address_:
            return x.apology('You must enter an address.', 'dashobard.send_greencard', id = request_id)
        
        plate_ = request.form.get('plate')
        if not plate_ or not x.valid_plate(plate_):
            return x.apology('Invalid plate.', 'dashboard.send_greencard', id = request_id)
        
        vin_ = request.form.get('vin')
        if not vin_ or not x.valid_vin(vin_):
            return x.apology('Invalid VIN.', 'dashboard.send_greencard', id = request_id)

        brand_ = request.form.get('brand')
        if not brand_ or not x.valid_brand(brand_):
            return x.apology('Invalid brand.', 'dashboard.send_greencard', id = request_id)
        
        type__ = request.form.get('type')
        if not type__ or not x.valid_type(type__):
            return x.apology('Invalid type.', 'dashboard.send_greencard', id = request_id)
        
        color_ = request.form.get('color')
        if not color_ or not x.valid_color(color_):
            return x.apology('Invalid color.', 'dashboard.send_greencard', id = request_id)
        
        start_date_ = request.form.get('start_date')
        if not start_date_ or not x.valid_startdate(start_date_):
            return x.apology('Invalid start date.', 'dashboard.send_greencard', id = request_id)
        
        policy_no_ = request.form.get('policy_no')
        if not policy_no_:
            return x.apology('You must enter policy number.', 'dashboard.send_greencard', id = request_id)
        
        period_ = request.form.get('period')
        if not period_ or period_ not in ['3M', '1M', '15D']:
            return x.apology('Invalid period.', 'dashboard.send_greencard', id = request_id)
        
        # ENG: Convert periods to readable strings
        # TR: Okunabilirlik için periyotları açıklanmış stringlere çevir
        if period_ == '15D':
            period_ = '15 Days'
        
        elif period_ == '1M':
            period_ = '1 Month'

        elif period_ == '3M':
            period_ = '3 Month'
        
        # ENG: Convert form data into dictionary for template
        # TR: Formdan gelen verileri şablona işlemek için dictionary haline getir
        requ = dict(
            name = name_,
            address = address_,
            plate = plate_,
            vin = vin_,
            brand = brand_,
            model = type__,
            color = color_,
            start_date = x.valid_date(start_date_),
            policy_no = policy_no_,
            period = period_,
            subject = f'For {period_} - FI {policy_no_} - From {x.valid_date(start_date_)}'
        )

        # ENG: Render template
        # TR: Şablonu renderla
        template = render_template('mail_template.html', requ = requ)

        # ENG: Prepare message
        # TR: Mesajı hazırla
        msg = Message(subject = requ['subject'], recipients = ['setmailsetting'], html = template)

        # ENG: Send mail
        # TR: Maili gönder
        try:
            from app import mail # ENG: Temporarily importing mail to avoid circular import / TR: Circular importtan kaçmak için geçici import yaptım
            mail.send(msg)
            try:
                # ENG: Update green card request status
                # TR: Yeşil sigorta talebinin durumunu güncelle
                DataBase.execute('UPDATE gc_requests SET status = 1 WHERE id = ? AND status = 0', request_id)
            except ValueError:
                return x.apology('Mail order created but status of request could not updated. Please ask for help to administrator.', 'dashboard.pending_greencards')
            return x.apology(f'The mailorder has been successfully created for vehicle with plate {plate_}.', 'dashboard.pending_greencards')
        
        except Exception as exc:
            return x.apology(f'An error occurred: {exc}', 'dashboard.pending_greencards')

    else:
        # ENG: Get request_id from args
        # TR: Request_id args'dan al
        requ_id = request.args.get('id')
        if not requ_id or not requ_id.isdigit():
            return redirect(url_for('dashboard.pending_greencards'))

        # ENG: Check if the request exists
        # TR: Talep mevcut mu sorgula
        gc_requ = DataBase.execute(x.file_query('unconfirmed_gc_request.sql'), requ_id)
        if not gc_requ or len(gc_requ) != 1:
            return x.apology('The request could not found or already sent.', 'dashboard.pending_greencards')

        # ENG: Render order page with request info
        # TR: Sipariş sayfasını talep bilgileriyle birlikte render et
        return render_template('gc_mailorder.html', greencard = gc_requ[0], periods = ['3M', '1M', '15D'])


# ENG: Complete green card process
# TR: Yeşil sigorta işlemini tamamlama
@dbbp.route('/greencard_requests/prepared', methods=['GET', 'POST'])
@x.login_required('employee')
def prepared_greencard():
    if request.method == 'POST':
        request_id = request.args.get('id')
        if not request_id or not request_id.isdigit():
            return redirect(url_for('dashboard.pending_greencards'))
        
        # ENG: Check if request is in "preparing" status
        # TR: Talep 'hazırlanıyor' durumunda mı kontrol et
        request_data = DataBase.execute('SELECT * FROM gc_requests WHERE id = ? AND status = 1', request_id)
        if not request_data or len(request_data) != 1:
            return x.apology('The request could not found or already prepared.', 'dashboard.pending_greencards')
        
        # ENG: Update request as "ready"
        # TR: Talebi 'hazırlandı' olarak güncelle
        try:
            DataBase.execute('UPDATE gc_requests SET status = 2 WHERE id = ? AND status = 1', request_id)
            return x.apology('The request status has been updated to "ready."', 'dashboard.pending_greencards')
        
        except ValueError:
            return x.apology('An error occurred. Try again.', 'dashboard.pending_requests')

    else:
        return redirect(url_for('dashboard.pending_greencards'))


# ENG: Route for canceling green card request
# TR: Yeşil sigorta talebini iptal etme rotası
@dbbp.route('/greencard_requests/cancel', methods=['GET', 'POST'])
@x.login_required('employee')
def cancel_gc_request():
    if request.method == 'POST':
        request_id = request.args.get('id')
        if not request_id or not request_id.isdigit():
            return redirect(url_for('dashboard.pending_greencards'))
        
        # ENG: Check if request is not completed
        # TR: Yeşil sigorta talebi tamamlanmamış durumda mı kontrol et
        request_data = DataBase.execute('SELECT * FROM gc_requests WHERE id = ? AND status != 2', request_id)
        if not request_data or len(request_data) != 1:
            return x.apology('The request could not found or already prepared.', 'dashboard.pending_greencards')
        
        # ENG: Cancel the request (race conditions considered)
        # TR: Talebi iptal et (Race conditions sebebiyle özellikle 'status != 2' ile siliyoruz)
        try:
            DataBase.execute('DELETE FROM gc_requests WHERE id = ? AND status != 2', request_id)
            return x.apology('The request status has been successfully cancelled.', 'dashboard.pending_greencards')

        except ValueError:
            return x.apology('An error occurred. Please try again.', 'dashboard.pending_greencards')
    else:
        return redirect(url_for('dashboard.pending_greencards'))
    

# ENG: All visa requests
# TR: Tüm vize talepleri
@dbbp.route('/visa_requests_all')
@x.login_required
def all_visas():
    visas = DataBase.execute(x.file_query('all_visa_requests.sql'))
    
    return render_template('all_visas.html', visas = visas, visa_count = len(visas))


# ENG: Pending visa appointments
# TR: Randevu bekleyen vize talepleri
@dbbp.route('/visa_requests')
@x.login_required('employee')
def pending_visas():
    visas = DataBase.execute(x.file_query('pending_visa_requests.sql'))

    return render_template('visa_requests.html', visas = visas)


# ENG: Confirm appointment date
# TR: Randevu tarihi kesinleştirme
@dbbp.route('/visa_requests/confirm_date', methods=['GET', 'POST'])
@x.login_required('employee')
def confirm_date():
    if request.method == 'POST':
        request_id = request.form.get('request_id')
        if not request_id or not request_id.isdigit():
            return redirect('dashboard.pending_visas')
        
        # ENG: Check if request is still pending appointment
        # TR: Talep hala randevu tarihi bekliyor mu kontrol et
        visa = DataBase.execute(x.file_query('pending_visa_request_paid.sql'), request_id)
        if not visa or len(visa) != 1:
            return x.apology('The request could not found or appointment date already confirmed or not paid.', 'dashboard.pending_visas')
        
        # ENG: Get confirmed date from form
        # TR: Kesinleştirilmiş tarihi formdan al
        confirmed_date = request.form.get('confirmed_date')
        if not confirmed_date or not x.valid_date(confirmed_date):
            return x.apology('Appointment date is invalid.', 'dashboard.pending_visas')

        # ENG: Add appointment date and update request status
        # TR: Randevu tarihini ekle ve talep durumunu güncelle
        try:
            DataBase.execute('UPDATE visa_requests SET status = 1, appointment_date = ? WHERE id = ? AND status = 0', x.valid_date(confirmed_date), request_id)
            return x.apology('The appointment date of the request has been successfully confirmed.', 'dashboard.pending_visas')
        
        except ValueError:
            return x.apology('An error occurred, please try again.', 'dashboard.pending_visas')
        
    else:
        requ_id = request.args.get('id')
        if not requ_id or not requ_id.isdigit():
            return redirect(url_for('dashboard.pending_visas'))
        
        # ENG: Check the status of the request
        # TR: Talep durumunu kontrol et
        visa_data = DataBase.execute(x.file_query('pending_visa_request.sql'), requ_id)
        if not visa_data or len(visa_data) != 1:
            return x.apology('The request could not found or appointment date already confirmed.', 'dashboard.pending_visas')

        return render_template('date_confirmation.html', visa = visa_data[0])
    
# ENG: Update payment status as "paid"
# TR: Ödeme durumunu 'ödendi' olarak güncelleme
@dbbp.route('/visa_requests/set_paid', methods = ['GET', 'POST'])
@x.login_required('employee')
def set_paid():
    if request.method == 'POST':
        request_id = request.form.get('id')
        if not request_id or not request_id.isdigit():
            return redirect(url_for('dashboard.pending_visas'))
        
        # ENG: Check request with unpaid status
        # TR: Talebi 'ödenmemiş ödeme durumu' ile sorgula
        request_data = DataBase.execute(x.file_query('pending_visa_request_unpaid.sql'), request_id)
        if not request_data or len(request_data) != 1:
            return x.apology('The request could not found or already paid.', 'dashboard.pending_visas')
        
        # ENG: Update payment status as "paid"
        # TR: Ödeme durumunu 'ödendi' güncelle
        try:
            DataBase.execute('UPDATE visa_requests SET payment_status = 1 WHERE id = ? AND status = 0 AND payment_status = 0', request_id)
            return x.apology('The payment status of the request has been successfully updated to "Paid"', 'dashboard.pending_visas')
        
        except ValueError:
            return x.apology('An error occurred, please try again.', 'dashboard.pending_visas')

    else:
        return render_template('visa_requests.html')
    

# ENG: Route for canceling visa request
# TR: Vize talebini iptal etme rotası
@dbbp.route('/visa_requests/cancel', methods=['GET', 'POST'])
@x.login_required('employee')
def cancel_visa_request():
    if request.method == 'POST':
        request_id = request.form.get('id')
        if not request_id or not request_id.isdigit():
            return redirect(url_for('dashboard.pending_visas'))
        
        # ENG: Check if request is in "pending appointment" status
        # TR: Talep 'randevu bekleme' durumunda mı kontrol et
        request_data = DataBase.execute('SELECT id FROM visa_requests WHERE id = ? AND status = 0', request_id)
        if not request_data or len(request_data) != 1:
            return x.apology("This request is already confirmed or cancelled.", 'dashboard.pending_visas')
        
        # ENG: Cancel the request (delete from database)
        # TR: Talebi iptal et (veritabanından sil)
        try:
            DataBase.execute('DELETE FROM visa_requests WHERE id = ? AND status = 0', request_id)
            return x.apology('The request has been successfully cancelled.', 'dashboard.pending_visas')
        
        except ValueError:
            return x.apology('An error occurred, please try again.', 'dashboard.pending_visas')
    
    else:
        return redirect(url_for('dashboard.pending_visas'))
    

# ENG: Approved visa requests
# TR: Randevu tarihi kesinleştirilmiş vize talepleri
@dbbp.route('/visa_requests/approved_visas')
@x.login_required('employee')
def approved_visas():
    approved = DataBase.execute(x.file_query('approved_visa_requests.sql'))
    
    return render_template('approved_visa_requests.html', visas = approved)


# ENG: Route to set request as "awaiting result"
# TR: Talebi 'sonuç aşaması' olarak ayarlama rotası
@dbbp.route('/visa_requests/approved_visas/visa_applicated', methods=['GET', 'POST'])
@x.login_required('employee')
def visa_applicated():
    if request.method == 'POST':
        request_id = request.form.get('id')
        if not request_id or not request_id.isdigit():
            return redirect(url_for('dashboard.approved_visas'))
        
        # ENG: Check if request is in "confirmed appointment" status
        # TR: Talep 'randevusu kesinleştirilmiş' durumda mı kontrol et
        visa_data = DataBase.execute(x.file_query('approved_visa_request.sql'), request_id)
        if not visa_data or len(visa_data) != 1:
            return x.apology('The request could not found or already applicated.', 'dashboard.approved_visas')
        
        # ENG: Get reference number from form
        # TR: Referans numarasını formdan al
        ref_no = request.form.get('ref_no')
        if not ref_no or len(ref_no) > 40:
            return x.apology('Invalid reference number.', 'dashboard.visa_applicated', id = request_id)

        # ENG: Update request status to "awaiting result" and insert reference number
        # TR: Talebin durumunu 'sonuç bekleniyor' olarak güncelle ve referans numarasını veritabanına gir
        try:
            DataBase.execute('UPDATE visa_requests SET status = 2 WHERE id = ? AND status = 1', request_id)
            DataBase.execute('INSERT INTO app_references (pass_id, request_id, reference_no) VALUES(?, ?, ?)', visa_data[0]['pass_id'], request_id, ref_no.upper())
            return x.apology('Request has been successfully updated to "Appliacted."', 'dashboard.approved_visas')
        
        except ValueError:
            return x.apology('An error occurred, please try again.', 'dashboard.visa_applicated', id = request_id)
    
    else:
        requ_id = request.args.get('id')
        if not requ_id or not requ_id.isdigit():
            return redirect(url_for('dashboard.approved_visas'))
        
        # ENG: Check if request is in "confirmed appointment" status
        # TR: Talep 'randevu tarihi kesinleştirilmiş' durumda mı kontrol et
        visa = DataBase.execute(x.file_query('approved_visa_request.sql'), requ_id)
        if not visa or len(visa) != 1:
            return x.apology('The request could not found or already applicated.', 'dashboard.approved_visas')

        return render_template('visa_applicated.html', visa = visa[0])

# ENG: Track visa application
# TR: Başvuru takibi
@dbbp.route('/visa_requests/approved_visas/track_request' , methods = ['GET', 'POST'])
@x.login_required('employee')
def visa_tracking():
    if request.method == 'POST':
        req_id = request.form.get('id')
        if not req_id or not req_id.isdigit():
            return redirect(url_for('dashboard.visa_tracking'))
        
        # ENG: Check if request is in "awaiting result" status
        # TR: Talep 'sonuç bekleniyor' durumunda mı kontrol et
        req_data = DataBase.execute(x.file_query('applicated_visa_request.sql'), req_id)
        if not req_data or len(req_data) != 1:
            return x.apology('Application could not found or already resulted.', 'dashboard.visa_tracking')
        
        # ENG: Update request as "resulted"
        # TR: Talebi 'sonuçlandı' olarak güncelle 
        try:
            DataBase.execute('UPDATE visa_requests SET status = 3, result_date = ? WHERE id = ? AND status = 2', datetime.today().date().strftime('%d/%m/%Y'), req_id)
            return x.apology('Application has been successfully resulted.', 'dashboard.visa_tracking')
        
        except ValueError:
            return x.apology('An error occurred, please try again.', 'dashboard.visa_tracking')

    else:
        # ENG: Query pending applications
        # TR: Sonuç bekleyen talepleri sorgula
        visas = DataBase.execute(x.file_query('applicated_visa_requests.sql'))

        return render_template('tracking_visa.html', visas = visas)