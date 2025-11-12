from .imports import *


dbbp = Blueprint("dashboard", __name__, url_prefix="/dashboard")


@dbbp.route('/')
@x.login_required('employee')
def employee_db():
    count_unconfirmed_passports = DataBase.execute('SELECT COUNT(*) AS count FROM passports WHERE confirmed != 1')
    
    count_awaiting_visa_requests = DataBase.execute('SELECT COUNT(*) AS count FROM visa_requests WHERE status = 0')

    count_confirmed_visa_appointment = DataBase.execute('SELECT COUNT(*) AS count FROM visa_requests WHERE status = 1')

    count_awaiting_gc_requests = DataBase.execute('SELECT COUNT(*) AS count FROM gc_requests WHERE status = 0')

    return render_template('employee_dashboard.html',
                           passports = count_unconfirmed_passports[0],
                           waiting_visa = count_awaiting_visa_requests[0],
                           confirmed_visa = count_confirmed_visa_appointment[0],
                           waiting_gc = count_awaiting_gc_requests[0])


@dbbp.route('/confirmation')
@x.login_required('employee')
def passport_confirmation():
    passports = DataBase.execute('SELECT users.username, passports.id, passports.name, passports.surname, passports.pass_no, passports.sex, passports.birth, passports.pass_exp, passports.ident_no FROM passports JOIN users ON passports.user_id = users.id WHERE passports.confirmed = 0')
    if not passports:
        return x.apology('There is no passports to confirm.', 'dashboard.employee_db')
    
    return render_template('passport_confirmation.html', passports = passports)


@dbbp.route('/confirmation/confirm', methods = ['POST'])
@x.login_required('employee')
def confirm_passport():
    # Pasaport id sini al
    # Pasaportu ve onayın durumunu kontrol et
        # Zaten onaylanmışsa yönlendir
    # Pasaportun confirmini güncelle (try-except)
    # Passport_confirmation sayfasına yönlendir
    pass


@dbbp.route('/confirmation/decline', methods = ['POST'])
@x.login_required('employee')
def decline_passport():
    # Pasaport id sini al
    # Pasaportu ve onayın durumunu kontrol et
        # Zaten onaylanmışsa yönlendir
    # Pasaportu sil (try-except)
    # Passport_confirmation sayfasına yönlendir
    pass