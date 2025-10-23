from .imports import *


dashboardbp = Blueprint("dashboard", __name__, url_prefix="/dashboard")


@dashboardbp.route("/user")
@x.login_required
def user_dashboard():
    return render_template("user_dashboard.html")


@dashboardbp.route("/employee")
@x.login_required("employee")
def employee_dashboard():
    return render_template("employee_dashboard.html")


@dashboardbp.route("/admin")
@x.login_required("admin")
def admin_dashboard():
    return render_template("admin_dashboard.html")


@dashboardbp.route("/vehicles")
@x.login_required
def vehicles():
    return render_template("my_vehicles.html")


@dashboardbp.route("/add_vehicle")
@x.login_required
def add_vehicle():
    return render_template("add_vehicle.html")