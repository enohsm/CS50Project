from .imports import *


dbbp = Blueprint("dashboard", __name__, url_prefix="/dashboard")


@dbbp.route('/')
@x.login_required('employee')
def employee_db():
    count_all_visa_requests = DataBase.execute('SELECT COUNT(*) AS count FROM visa_requests')

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
                           applicated_visa = count_applicated_visa_requests[0])


@dbbp.route('/confirmation')
@x.login_required('employee')
def passport_confirmation():
    passports = DataBase.execute('SELECT users.username, passports.id, passports.name, passports.surname, passports.pass_no, passports.sex, passports.birth, passports.pass_exp, passports.ident_no FROM passports JOIN users ON passports.user_id = users.id WHERE passports.confirmed = 0')
    
    return render_template('passport_confirmation.html', passports = passports)


@dbbp.route('/confirmation/confirm', methods = ['GET', 'POST'])
@x.login_required('employee')
def confirm_passport():
    if request.method == 'POST':
        # Pasaport id sini al
        pass_id = request.args.get('id')
        if not pass_id or not pass_id.isdigit():
            return redirect(url_for('dashboard.passport_confirmation'))
        
        # Pasaportu ve onayın durumunu kontrol et
        pass_data = DataBase.execute('SELECT * FROM passports WHERE id = ? AND confirmed = 0', pass_id)
        if not pass_data or len(pass_data) != 1:
            return x.apology('Passport could not found or already confirmed.', 'dashboard.passport_confirmation')
        
        # Pasaportun confirmini güncelle (try-except)
        try:
            DataBase.execute('UPDATE passports SET confirmed = 1 WHERE id = ?', pass_id)
            return x.apology(f'The passport with number {pass_data[0]['pass_no']} has been successfully approved.', 'dashboard.passport_confirmation')
        
        except ValueError:
            return x.apology('An error occurred. Please try again.', 'dashboard.passport_confirmation')
        
    else:
        return redirect(url_for('dashboard.passport_confirmation'))


@dbbp.route('/confirmation/cancel', methods = ['GET', 'POST'])
@x.login_required('employee')
def cancel_passport():
    if request.method == 'POST':
        # Pasaport id sini al
        pass_id = request.args.get('id')
        if not pass_id or not pass_id.isdigit():
            return redirect(url_for('dashboard.passport_confirmation'))
        
        # Pasaportu ve onayın durumunu kontrol et
        pass_data = DataBase.execute('SELECT * FROM passports WHERE id = ? AND confirmed = 0', pass_id)
        if not pass_data or len(pass_data) != 1:
            return x.apology('Passport could not found or already confirmed.', 'dashboard.passport_confirmation')
        
        # Pasaportu sil (try-except)
        try:
            DataBase.execute('DELETE FROM passports WHERE id = ?', pass_id)
            if os.path.exists(f'static/passports/{pass_data[0]['img']}'):
                os.remove(f'static/passports/{pass_data[0]['img']}')
            return x.apology(f'The passport with number {pass_data[0]['pass_no']} has been successfully cancelled.', 'dashboard.passport_confirmation')

        except:
            return x.apology('An error occurred. Please try again.', 'dashboard.passport_confirmation')
        
    else:
        return redirect(url_for('dashboard.passport_confirmation'))
    

@dbbp.route('/greencard_requests')
@x.login_required('employee')
def pending_greencards():
    gc_requests = DataBase.execute(x.file_query('pending_gc_requests.sql'))

    return render_template('greencard_requests.html', greencards = gc_requests)


@dbbp.route('/greencard_requests/send', methods=['GET', 'POST'])
@x.login_required('employee')
def send_greencard():
    if request.method == 'POST':
        request_id = request.form.get('request_id')
        if not request_id or not request_id.isdigit():
            return redirect(url_for('dashboard.pending_greencards'))
        
        is_exist_request = DataBase.execute('SELECT * FROM gc_requests WHERE id = ? AND status = 0', request_id)
        if not is_exist_request:
            return x.apology('This request is not pending.', 'dashboard.pending_greencards')
        
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
        if not type_ or not x.valid_type(type__):
            return x.apology('Invalid type.', 'dashboard.send_greencard', id = request_id)
        
        color_ = request.form.get('color')
        if not color or not x.valid_color(color_):
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
        
        request = dict(
            name = name_,
            address = address_,
            plate = plate_,
            vin = vin_,
            brand = brand_,
            model = type__,
            color = color_,
            start_date = start_date_,
            policy_no = policy_no_,
            period = period_
        )

    else:
        # Request_id args'dan al
        requ_id = request.args.get('id')
        if not requ_id or not requ_id.isdigit():
            return redirect(url_for('dashboard.pending_greencards'))

        # Request'i file_query(unconfirmed_gc_request.sql) ile sorgula
        gc_requ = DataBase.execute(x.file_query('unconfirmed_gc_request.sql'), requ_id)
        if not gc_requ or len(gc_requ) != 1:
            return x.apology('The request could not found or already sent.', 'dashboard.pending_greencards')

        return render_template('gc_mailorder.html', greencard = gc_requ[0], periods = ['3M', '1M', '15D'])



@dbbp.route('/greencard_requests/prepared', methods=['GET', 'POST'])
@x.login_required('employee')
def prepared_greencard():
    if request.method == 'POST':
        request_id = request.args.get('id')
        if not request_id or not request_id.isdigit():
            return redirect(url_for('dashboard.pending_greencards'))
        
        request_data = DataBase.execute('SELECT * FROM gc_requests WHERE id = ? AND status = 1', request_id)
        if not request_data or len(request_data) != 1:
            return x.apology('The request could not found or already prepared.', 'dashboard.pending_greencards')
        
        try:
            DataBase.execute('UPDATE gc_requests SET status = 2 WHERE id = ? AND status = 1', request_id)
            return x.apology('The request status has been updated to "ready."', 'dashboard.pending_greencards')
        
        except ValueError:
            return x.apology('An error occurred. Try again.', 'dashboard.pending_requests')

    else:
        return redirect(url_for('dashboard.pending_greencards'))


@dbbp.route('/greencard_requests/cancel', methods=['GET', 'POST'])
@x.login_required('employee')
def cancel_gc_request():
    if request.method == 'POST':
        request_id = request.args.get('id')
        if not request_id or not request_id.isdigit():
            return redirect(url_for('dashboard.pending_greencards'))
        
        request_data = DataBase.execute('SELECT * FROM gc_requests WHERE id = ? AND status != 2', request_id)
        if not request_data or len(request_data) != 1:
            return x.apology('The request could not found or already prepared.', 'dashboard.pending_greencards')
        
        try:
            DataBase.execute('DELETE FROM gc_requests WHERE id = ? AND status != 2', request_id)
            return x.apology('The request status has been successfully cancelled.', 'dashboard.pending_greencards')

        except ValueError:
            return x.apology('An error occurred. Please try again.', 'dashboard.pending_greencards')
    else:
        return redirect(url_for('dashboard.pending_greencards'))
    

@dbbp.route('/visa_requests_all')
@x.login_required
def all_visas():
    visas = DataBase.execute(x.file_query('all_visa_requests.sql'))
    
    return render_template('all_visas.html', visas = visas, visa_count = len(visas))


@dbbp.route('/visa_requests')
@x.login_required('employee')
def pending_visas():
    visas = DataBase.execute(x.file_query('pending_visa_requests.sql'))

    return render_template('visa_requests.html', visas = visas)


@dbbp.route('/visa_requests/confirm_date', methods=['GET', 'POST'])
@x.login_required('employee')
def confirm_date():
    if request.method == 'POST':
        request_id = request.form.get('request_id')
        if not request_id or not request_id.isdigit():
            return redirect('dashboard.pending_visas')
        
        visa = DataBase.execute(x.file_query('pending_visa_request_paid.sql'), request_id)
        if not visa or len(visa) != 1:
            return x.apology('The request could not found or appointment date already confirmed or not paid.', 'dashboard.pending_visas')
        
        confirmed_date = request.form.get('confirmed_date')
        if not confirmed_date or not x.valid_date(confirmed_date):
            return x.apology('Appointment date is invalid.', 'dashboard.pending_visas')

        try:
            DataBase.execute('UPDATE visa_requests SET status = 1, appointment_date = ? WHERE id = ? AND status = 0', x.valid_date(confirmed_date), request_id)
            return x.apology('The appointment date of the request has been successfully confirmed.', 'dashboard.pending_visas')
        
        except ValueError:
            return x.apology('An error occurred, please try again.', 'dashboard.pending_visas')
        
    else:
        requ_id = request.args.get('id')
        if not requ_id or not requ_id.isdigit():
            return redirect(url_for('dashboard.pending_visas'))

        visa_data = DataBase.execute(x.file_query('pending_visa_request.sql'), requ_id)
        if not visa_data or len(visa_data) != 1:
            return x.apology('The request could not found or appointment date already confirmed.', 'dashboard.pending_visas')

        return render_template('date_confirmation.html', visa = visa_data[0])
    

@dbbp.route('/visa_requests/set_paid', methods = ['GET', 'POST'])
@x.login_required('employee')
def set_paid():
    if request.method == 'POST':
        request_id = request.form.get('id')
        if not request_id or not request_id.isdigit():
            return redirect(url_for('dashboard.pending_visas'))
        
        request_data = DataBase.execute(x.file_query('pending_visa_request_unpaid.sql'), request_id)
        if not request_data or len(request_data) != 1:
            return x.apology('The request could not found or already paid.', 'dashboard.pending_visas')
        
        try:
            DataBase.execute('UPDATE visa_requests SET payment_status = 1 WHERE id = ? AND status = 0 AND payment_status = 0', request_id)
            return x.apology('The payment status of the request has been successfully updated to "Paid"', 'dashboard.pending_visas')
        
        except ValueError:
            return x.apology('An error occurred, please try again.', 'dashboard.pending_visas')

    else:
        return render_template('visa_requests.html')
    

@dbbp.route('/visa_requests/cancel', methods=['GET', 'POST'])
@x.login_required('employee')
def cancel_visa_request():
    if request.method == 'POST':
        request_id = request.form.get('id')
        if not request_id or not request_id.isdigit():
            return redirect(url_for('dashboard.pending_visas'))
        
        request_data = DataBase.execute('SELECT id FROM visa_requests WHERE id = ? AND status = 0', request_id)
        if not request_data or len(request_data) != 1:
            return x.apology("This request is already confirmed or cancelled.", 'dashboard.pending_visas')
        
        try:
            DataBase.execute('DELETE FROM visa_requests WHERE id = ? AND status = 0', request_id)
            return x.apology('The request has been successfully cancelled.', 'dashboard.pending_visas')
        
        except ValueError:
            return x.apology('An error occurred, please try again.', 'dashboard.pending_visas')
    
    else:
        return redirect(url_for('dashboard.pending_visas'))
    

@dbbp.route('/visa_requests/approved_visas')
@x.login_required('employee')
def approved_visas():
    approved = DataBase.execute(x.file_query('approved_visa_requests.sql'))
    
    return render_template('approved_visa_requests.html', visas = approved)


@dbbp.route('/visa_requests/approved_visas/visa_applicated', methods=['GET', 'POST'])
@x.login_required('employee')
def visa_applicated():
    if request.method == 'POST':
        request_id = request.form.get('id')
        if not request_id or not request_id.isdigit():
            return redirect(url_for('dashboard.approved_visas'))
        
        visa_data = DataBase.execute(x.file_query('approved_visa_request.sql'), request_id)
        if not visa_data or len(visa_data) != 1:
            return x.apology('The request could not found or already applicated.', 'dashboard.approved_visas')
        
        ref_no = request.form.get('ref_no')
        if not ref_no or len(ref_no) > 40:
            return x.apology('Invalid reference number.', 'dashboard.visa_applicated', id = request_id)

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
        
        visa = DataBase.execute(x.file_query('approved_visa_request.sql'), requ_id)
        if not visa or len(visa) != 1:
            return x.apology('The request could not found or already applicated.', 'dashboard.approved_visas')

        return render_template('visa_applicated.html', visa = visa[0])


@dbbp.route('/visa_requests/approved_visas/track_request' , methods = ['GET', 'POST'])
@x.login_required('employee')
def visa_tracking():
    if request.method == 'POST':
        req_id = request.form.get('id')
        if not req_id or not req_id.isdigit():
            return redirect(url_for('dashboard.visa_tracking'))
        
        req_data = DataBase.execute(x.file_query('applicated_visa_request.sql'), req_id)
        if not req_data or len(req_data) != 1:
            return x.apology('Application could not found or already resulted.', 'dashboard.visa_tracking')
        
        try:
            DataBase.execute('UPDATE visa_requests SET status = 3, result_date = ? WHERE id = ? AND status = 2', datetime.today().date().strftime('%d/%m/%Y'), req_id)
            return x.apology('Application has been successfully resulted.', 'dashboard.visa_tracking')
        
        except ValueError:
            return x.apology('An error occurred, please try again.', 'dashboard.visa_tracking')

    else:
        visas = DataBase.execute(x.file_query('applicated_visa_requests.sql'))

        return render_template('tracking_visa.html', visas = visas)