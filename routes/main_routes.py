from .imports import *


# ENG: Assign variable for blueprint of main routes
# TR: "main" rotalarını modülleyecek bir değişken ata
mainbp = Blueprint("main", __name__)

# ENG: Some user operations are handled within the "main" routes.
# TR: "main" rotaları kullanıcı işlemlerinin de bir kısmını kapsar.

@mainbp.route("/")
def homepage():
    return render_template("homepage.html")


@mainbp.route("/register")
def register():
    return render_template("register.html")


@mainbp.route("/login")
def login():
    return render_template("login.html")


@mainbp.route("/logout")
def logout():
    return "TODO"