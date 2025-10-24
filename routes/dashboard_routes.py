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


@dashboardbp.route("/add_vehicle", methods=["GET", "POST"])
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
        
        vehicles = DataBase.execute("SELECT plate FROM vehicles WHERE user_id = ? AND plate = ?", session["user_id"], plate)
        if vehicles:
            flash("This vehicle is already in your vehicle list.")
            return (url_for("dashboard.add_vehicle"))
        
        DataBase.execute("INSERT INTO vehicles (user_id, namesurname, address, plate, vin, brand, model, color) VALUES(?, ?, ?, ?, ?, ?, ?, ?)", session["user_id"], name.upper(), (district.upper()+"/"+province.upper()), plate.upper(), vin.upper(), brand.upper(), type.upper(), color.upper())
        flash("Your vehicle has successfully registered.")
        return redirect(url_for("profile.vehicles"))
    else:
        return render_template("add_vehicle.html")


@dashboardbp.route("/passports")
@x.login_required
def passports():
    return render_template("my_passports.html")


@dashboardbp.route("/add_passport")
@x.login_required
def add_passport():
    return render_template("add_passport.html")