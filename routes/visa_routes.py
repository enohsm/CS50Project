from .imports import *


# ENG: Assign variable for blueprint of visa routes
# TR: Vize rotalarını modülleyecek bir değişken ata
visabp = Blueprint("visa", __name__, url_prefix="/visa")


@visabp.route("/")
def aboutvisa():
    return render_template("visa.html")


@visabp.route("/request")
@x.login_required
def visaapp():
    return render_template("visa_.html")


@visabp.route("/status")
@x.login_required
def visastatus():
    return render_template("visa_app_status.html")


@visabp.route("/statistics")
@x.login_required
def visastatistics():
    return render_template("visa_app_statistics.html")


@visabp.route("/application")
@x.login_required("employee")
def visa_application():
    return render_template("visa_application.html")