from .imports import *


# ENG: Assign a variable for the profile routes blueprint
# TR: Profil rotalarını modülleyecek bir değişken ata
profilebp = Blueprint("profile", __name__, url_prefix="/me")

# Profil route ayarla
@profilebp.route("/")
def profile():
    return render_template("profile.html")

# Araçlar routeunu ayarla
@profilebp.route("/vehicles")
def vehicles():
    return render_template("my_vehicles.html")

# Pasaportlar routeunu ayarla
@profilebp.route("/passports")
def passports():
    return render_template("my_passports.html")

# Visa requests routeunu ayarla
@profilebp.route("/requests")
def requests():
    return render_template("requests.html")