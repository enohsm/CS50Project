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