from .imports import *


# ENG: Assign variable for blueprint of green card routes
# TR: Yeşil sigorta rotalarını modülleyecek bir değişken ata
gcbp = Blueprint("greencard", __name__, url_prefix="/greencard")


@gcbp.route("/")
def greenmain():
    return render_template("greencard.html")


@gcbp.route("/request")
def greenrequest():
    return render_template("greencard_request.html")


@gcbp.route("/status")
def greenstatus():
    return render_template("greencard_status.html")