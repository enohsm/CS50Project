from .imports import *


# ENG: Assign variable for blueprint of green card routes
# TR: Yeşil sigorta rotalarını modülleyecek bir değişken ata
gcbp = Blueprint("greencard", __name__, url_prefix="/greencard")


@gcbp.route("/")
def aboutgreen():
    return render_template("greencard.html")


@gcbp.route("/request")
@x.login_required
def greenrequest():
    return render_template("greencard_request.html")


@gcbp.route("/status")
@x.login_required
def greenstatus():
    return render_template("greencard_status.html")


@gcbp.route("/application")
@x.login_required("employee")
def greencard_application():
    return render_template("greencard_application.html")