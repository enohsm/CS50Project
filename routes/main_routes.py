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
    if request.method == "POST":
        # EN: Check the data received from the form
        # TR: Formdan gelen verileri kontrol et

        username = request.form.get("username")
        # EN:
        # TR: Kullanıcı adı girilmiş mi? 5 ile 20 karakter arasında mı?
        if not username or not 5 < len(username) < 20:
            flash("Invalid username.")
            return redirect("/register")

        password = request.form.get("password")
        # Şifre girilmiş mi? Pattern doğru mu? Uzunluk yeterli mi?
        if not password or :
            flash("Password cannot be empty.")
            return redirect("/register")

        confirmation = request.form.get("confirmation")
        if not confirmation:
            flash("Password confirmation cannot be empty.")
            return redirect("/register")
        
        name = request.form.get("name")
        surname = request.form.get("surname")
        if not name or not surname:
            flash("Name/Surname cannot be empty.")
            return redirect("/register")
        
        if not name.isalpha() or not surname.isalpha():
            flash("Only letters can be used for first name and last name")
            return redirect("/register")
        
        birth = request.form.get("birth")
        if not valid_date(birth):
            flash("Invalid birth date.")
        

        isexist = db.execute("SELECT username, password FROM users WHERE username = ?", username)
        if isexist:
            flash("This username already in use.")
            return redirect("/register")

        if match_passwords(password, confirmation):
            db.execute("INSERT INTO users (username, password, name, surname, birth, ident_no, email, contact) VALUES(username,)",)
            flash("You have successfully registered.")
            return redirect("/login")
    else:
        return render_template("register.html")


@mainbp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # EN: Check the data received from the form
        # TR: Formdan gelen verileri kontrol et
        username = request.form.get("username")
        if not username:
            flash("Username cannot be empty.")
            return redirect("/login")

        password = request.form.get("password")
        if not password:
            flash("Password cannot be empty.")
            return redirect("/login")
        
        # EN: Check if the user exists in the database
        # TR: Kullanıcı veritabanında var mı kontrol et
        user = db.execute("SELECT id, username, password FROM users WHERE username = ?", username)
        if not user:
            flash("Invalid username.")
            return redirect("/login")
        
        # EN: 
        # TR: Şifre eşleşmesini kontrol et
        if password != user[0]["password"]:
            flash("Invalid password.")
            return redirect("/login")
        
        # EN: If login is successful, save the user information to the session
        # TR: Giriş başarılıysa bilgileri session'a kaydet
        session["user_id"] = user[0]["id"]
        session["username"] = user[0]["username"]

        return redirect("/")
        
    else:
        return render_template("login.html")


@mainbp.route("/logout")
def logout():
    return "TODO"