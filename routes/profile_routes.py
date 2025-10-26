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


@profilebp.route("/vehicles/add", methods=["GET", "POST"])
@x.login_required
def add_vehicle():
    if request.method == "POST":
        name = request.form.get("name")
        if not name or not x.valid_name(name):
            flash("Invalid name")
            return redirect(url_for("dashboard.add_vehicle"))
        
        province = request.form.get("province")
        district = request.form.get("district")
        if not province or not district or not x.valid_location(province, district):
            flash("Invalid location.")
            return (url_for("dashboard.add_vehicle"))
        
        plate = request.form.get("plate")
        if not plate or not x.valid_plate(plate):
            flash("Invalid plate.")
            return (url_for("dashboard.add_vehicle"))
        
        vin = request.form.get("vin")
        if not vin or not x.valid_vin(vin):
            flash("Invalid VIN.")
            return (url_for("dashboard.add_vehicle"))
        
        brand = request.form.get("brand")
        if not brand or not x.valid_brand(brand):
            flash("Invalid brand.")
            return (url_for("dashboard.add_vehicle"))
        
        type = request.form.get("type")
        if not type or not x.valid_type(type):
            flash("Invalid type.")
            return (url_for("dashboard.add_vehicle"))
        
        color = request.form.get("color")
        if not color or not x.valid_color(color):
            flash("Invalid color.")
            return (url_for("dashboard.add_vehicle"))
        
        vehicles = DataBase.execute("SELECT id FROM vehicles WHERE user_id = ? AND plate = ?", session["user_id"], plate)
        if vehicles:
            flash("This vehicle is already in your vehicle list.")
            return (url_for("dashboard.add_vehicle"))
        
        DataBase.execute("INSERT INTO vehicles (user_id, namesurname, address, plate, vin, brand, model, color) VALUES(?, ?, ?, ?, ?, ?, ?, ?)", session["user_id"], name.upper(), (district.upper()+"/"+province.upper()), plate.upper(), vin.upper(), brand.upper(), type.upper(), color.upper())
        flash("Your vehicle has successfully registered.")
        return redirect(url_for("profile.vehicles"))
    else:
        return render_template("add_vehicle.html")
    

@profilebp.route("/vehicles/modify", methods=["GET", "POST"])
@x.login_required
def modify_vehicle():
    if request.method == "POST":
        vehicle_id = request.args.get("id")
        vehicle = DataBase.execute("SELECT * FROM vehicles WHERE id = ? AND user_id = ?", vehicle_id, session["user_id"])
        if len(vehicle) != 1:
            flash("Unauthorized access.")
            return redirect(url_for("profile.vehicles"))
        
        name
        
        DataBase.execute("UPDATE vehicles ")
        
    else:
        vehicle_id = request.args.get("id")
        vehicle = DataBase.execute("SELECT * FROM vehicles WHERE id = ? AND user_id = ?", vehicle_id, session["user_id"])
        if len(vehicle) != 1:
            flash("Unauthorized access.")
            return redirect(url_for("profile.vehicles"))
        return render_template("modify_vehicle.html", vehicle=vehicle[0])


@profilebp.route("/vehicles/delete")
@x.login_required
def delete_vehicle():
    return redirect(url_for("profile.vehicles"))
    

@profilebp.route("/passports/add")
@x.login_required
def add_passport():
    return render_template("add_passport.html")


@profilebp.route("/passports/modify")
@x.login_required
def modify_passport():
    return render_template("modify_passport.html")


@profilebp.route("/passports/delete")
@x.login_required
def delete_passport():
    return redirect(url_for("profile.passports"))