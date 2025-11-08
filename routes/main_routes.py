from .imports import *


# ENG: Assign variable for blueprint of main routes
# TR: "main" rotalarını modülleyecek bir değişken ata
mainbp = Blueprint("main", __name__)

# ENG: Some user operations are handled within the "main" routes.
# TR: "main" rotaları kullanıcı işlemlerinin de bir kısmını kapsar.

@mainbp.route("/")
def homepage():
    return render_template("homepage.html")


@mainbp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        if "user_id" in session:
            flash("You are already logged in.")
            return redirect("/")

        # EN: Check the data received from the form
        # TR: Formdan gelen verileri kontrol et

        username = request.form.get("username")
        # EN:
        # TR: Kullanıcı adı girilmiş mi? 5 ile 20 karakter arasında mı?
        if not username or not 5 <= len(username) <= 20:
            flash("Invalid username.")
            return redirect("/register")
        if x.isexisting("users", "username", username):
            flash("Username is already taken.")
            return redirect("/register")

        password = request.form.get("password")
        # Şifre girilmiş mi? Pattern doğru mu? Uzunluk yeterli mi?
        if not password or not x.valid_password(password):
            flash("Invalid password.")
            return redirect("/register")

        # Onay girilmiş mi? Şifre ile eşleşiyor mu?
        confirmation = request.form.get("confirmation")
        if not confirmation or not x.match_passwords(password, confirmation):
            flash("Passwords do not match.")
            return redirect("/register")
        
        # İsim girilmiş mi? Harf dışında karakter içeriyor mu?
        name = request.form.get("name")
        surname = request.form.get("surname")
        if not name or not surname or not x.valid_namesurname(name, surname):
            flash("Invalid name/surname.")
            return redirect("/register")
        
        sex = request.form.get("sex")
        if not sex or sex not in ["male", "female"]:
            flash("Invalid sex.")
            return redirect("/register")
        
        # Doğum tarihini formatı doğru mu?
        birth = request.form.get("birth")
        if not birth or not x.valid_birthdate(birth):
            flash("Invalid birth date.")
            return redirect("/register")

        # Kimlik numarası var mı? Rakamlardan mı oluşuyor? Uzunluğu doğru mu?
        ident_no = request.form.get("ident_no")
        if not ident_no or not x.valid_identification(ident_no):
            flash("Invalid identification number.")
            return redirect("/register")
        if x.isexisting("users", "ident_no", ident_no):
            flash("This identification number is already registered.")
            return redirect("/register")
        
        # Mail var mı? Formatı doğru mu?
        email = request.form.get("email")
        if not email or not x.valid_email(email):
            flash("Invalid email address.")
            return redirect("/register")
        if x.isexisting("users", "email", email):
            flash("This e-mail is already registered.")
            return redirect("/register")
        
        # Telefon numarası var mı?
        contact = request.form.get("contact")
        if not contact or not x.valid_contact(contact):
            flash("Invalid contact number.")
            return redirect("/register")
        if x.isexisting("users", "contact", contact):
            flash("This contact number is already registered.")
            return redirect("/register")

        # KAYIT
        try:
            DataBase.execute("INSERT INTO users (username, password, name, surname, sex, birth, ident_no, email, contact) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)", username, generate_password_hash(password), name.capitalize(), surname.capitalize(), sex.upper(), x.valid_date(birth), ident_no, email, contact)
            DataBase.execute("INSERT INTO roles (user_id) VALUES((SELECT id FROM users WHERE username = ?))", username)
            flash("You have successfully registered.")
            return redirect("/login")
        except ValueError:
            flash("An error occured, please try again.")
            return redirect('/register')
    else:
        if "user_id" in session:
            flash("You are already logged in.")
            return redirect("/")
        return render_template("register.html")


@mainbp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if "user_id" in session:
            flash("You are already logged in.")
            return redirect("/")
        
        # EN: Check the data received from the form
        # TR: Formdan gelen verileri kontrol et
        username = request.form.get("username")
        password = request.form.get("password")
        if not username or not password:
            flash("Username/password cannot be empty.")
            return redirect("/login")
        
        # EN: Check if the user exists in the database
        # TR: Kullanıcı veritabanında var mı kontrol et
        user = DataBase.execute("SELECT users.id, users.username, users.password, users.name, roles.role FROM users JOIN roles ON users.id = roles.user_id WHERE username = ?", username)
        if not user or not check_password_hash(user[0]["password"], password):
            flash("Invalid username/password.")
            return redirect("/login")
        
        # EN: If login is successful, save the user information to the session
        # TR: Giriş başarılıysa bilgileri session'a kaydet
        session["user_id"] = user[0]["id"]
        session["username"] = user[0]["username"]
        session["name"] = user[0]["name"]
        session["role"] = user[0]["role"]
        return redirect(url_for('main.homepage'))
        
    else:
        if "user_id" in session:
            flash("You are already logged in.")
            return redirect("/")
        return render_template("login.html")


@mainbp.route("/logout")
def logout():
    if not "user_id" in session:
        flash("You are already logged out.")
        return redirect("/")
    
    else:
        session.clear()
        flash("You have successfully logged out.")
        return redirect("/")