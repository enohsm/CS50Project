from .imports import *


dashboardbp = Blueprint("dashboard", __name__)


@dashboardbp.route("/user_dashboard")
@x.login_required
def user_dashboard():
    return render_template("user_dashboard.html")


@dashboardbp.route("/employee_dashboard")
@x.login_required("employee")
def employee_dashboard():
    return render_template("employee_dashboard.html")


@dashboardbp.route("/admin_dashboard")
@x.login_required("admin")
def admin_dashboard():
    return render_template("admin_dashboard.html")