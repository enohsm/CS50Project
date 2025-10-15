from .imports import *


# ENG: Assign variable for blueprint of visa routes
# TR: Vize rotalarını modülleyecek bir değişken ata
visabp = Blueprint("visa", __name__, url_prefix="/visa")


@visabp.route("/")
def aboutvisa():
    return render_template("visa.html")


@visabp.route("/application")
def visaapp():
    return render_template("visa_application.html")


@visabp.route("/status")
def visastatus():
    return render_template("visa_app_status.html")


@visabp.route("/statistics")
def visastatistics():
    return render_template("visa_app_statistics.html")