from .imports import *


# ENG: Assign variable for blueprint of main routes
# TR: "main" rotalarını modülleyecek bir değişken ata
mainbp = Blueprint("main", __name__)

# ENG: Assign variable to read the data from database
# TR: Veritabanından okunan veriyi bir değişkene atıyorum
db = SQL("sqlite:///database.db")

# ENG: Some user operations are handled within the "main" routes.
# TR: "main" rotaları kullanıcı işlemlerinin de bir kısmını kapsar.

@mainbp.route("/")
def homepage():
    return render_template("homepage.html")


@mainbp.route("/register")
def register():
    return render_template("register.html")


@mainbp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        if not username:
            flash("Username cannot be empty.")
            return redirect("/login")

        password = request.form.get("password")
        if not password:
            flash("Password cannot be empty.")
            return redirect("/login")
        
        user = db.execute("SELECT id, username, password FROM users WHERE username = ?", username)
        if not user:
            flash("Invalid username.")
            return redirect("/login")
        
        if password != user[0]["password"]:
            flash("Invalid password.")
            return redirect("/login")
        
        session["user_id"] = user[0]["id"]

        return("/")
        
    else:
        return render_template("login.html")


@mainbp.route("/logout")
def logout():
    return "TODO"