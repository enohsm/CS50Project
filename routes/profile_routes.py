from .imports import *


# ENG: Assign a variable for the profile routes blueprint
# TR: Profil rotalarını modülleyecek bir değişken ata
profilebp = Blueprint("profile", __name__, url_prefix="/me")

# Profil route ayarla
@profilebp.route("/")
@x.login_required
def profile():
    return render_template("profile.html")

# Araçlar routeunu ayarla
@profilebp.route("/vehicles")
@x.login_required
def vehicles():
    vehicles = DataBase.execute("SELECT * FROM vehicles WHERE user_id = ?", session["user_id"])
    return render_template("my_vehicles.html", vehicles=vehicles)


# Pasaportlar routeunu ayarla
@profilebp.route("/passports")
@x.login_required
def passports():
    return render_template("my_passports.html")

# Evraklar routeunu ayarla
@profilebp.route("/documents")
@x.login_required
def documents():
    return render_template("my_documents.html")

# Visa requests routeunu ayarla
@profilebp.route("/requests")
@x.login_required
def requests():
    return render_template("my_requests.html")

