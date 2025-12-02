from .imports import *


# ENG: Assign variable for blueprint of main routes
# TR: "main" rotalarını modülleyecek bir değişken ata
mainbp = Blueprint("main", __name__)

# ENG: Some user operations are handled within the "main" routes.
# TR: Bazı kullanıcı işlemleri "main" rotalarında ele alındı (anasayfa, kayıt olma, giriş yapma, çıkış yapma)

# ENG: Homepage route
# TR: Anasayfa yönlendirmesi
@mainbp.route("/")
def homepage():
    news = DataBase.execute("SELECT * FROM posts WHERE type = 'News' ORDER BY create_datetime DESC LIMIT 5")
    announcements = DataBase.execute("SELECT * FROM posts WHERE type = 'Announcement' ORDER BY create_datetime DESC LIMIT 5")

    return render_template("homepage.html", news = news, announcements = announcements)

# ENG: Registration route
# TR: Kayıt olma rotası
@mainbp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # ENG: User session check
        # TR: Kullanıcı oturum kontrolü
        if "user_id" in session:
            flash("You are already logged in.")
            return redirect("/")

        # ENG: Get data from form and validate
        # TR: Formdan verileri al ve kontrollerini yap
        username = request.form.get("username")
        if not username or not 5 <= len(username) <= 20:
            flash("Invalid username.")
            return redirect("/register")

        if x.isexisting("users", "username", username):
            flash("Username is already taken.")
            return redirect("/register")

        password = request.form.get("password")
        if not password or not x.valid_password(password):
            flash("Invalid password.")
            return redirect("/register")

        confirmation = request.form.get("confirmation")
        if not confirmation or not x.match_passwords(password, confirmation):
            flash("Passwords do not match.")
            return redirect("/register")
        
        name = request.form.get("name")
        surname = request.form.get("surname")
        if not name or not surname or not x.valid_namesurname(name, surname):
            flash("Invalid name/surname.")
            return redirect("/register")
        
        sex = request.form.get("sex")
        if not sex or sex not in ["male", "female"]:
            flash("Invalid sex.")
            return redirect("/register")
        
        birth = request.form.get("birth")
        if not birth or not x.valid_birthdate(birth):
            flash("Invalid birth date.")
            return redirect("/register")

        ident_no = request.form.get("ident_no")
        if not ident_no or not x.valid_identification(ident_no):
            flash("Invalid identification number.")
            return redirect("/register")
        if x.isexisting("users", "ident_no", ident_no):
            flash("This identification number is already registered.")
            return redirect("/register")
        
        email = request.form.get("email")
        if not email or not x.valid_email(email):
            flash("Invalid email address.")
            return redirect("/register")
        if x.isexisting("users", "email", email):
            flash("This e-mail is already registered.")
            return redirect("/register")
        
        contact = request.form.get("contact")
        if not contact or not x.valid_contact(contact):
            flash("Invalid contact number.")
            return redirect("/register")
        if x.isexisting("users", "contact", contact):
            flash("This contact number is already registered.")
            return redirect("/register")

        # ENG: Complete registration (Insert data into "users" and "roles" tables)
        # TR: Kayıt işlemini tamamla (Verileri "kullanıcılar" ve "roller" tablolarına ekle)
        try:
            DataBase.execute("INSERT INTO users (username, password, name, surname, sex, birth, ident_no, email, contact) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)", username, generate_password_hash(password), name.capitalize(), surname.capitalize(), sex.upper(), x.valid_date(birth), ident_no, email, contact)
            DataBase.execute("INSERT INTO roles (user_id) VALUES((SELECT id FROM users WHERE username = ?))", username)
            flash("You have successfully registered.")
            return redirect("/login")
        except ValueError:
            flash("An error occured, please try again.")
            return redirect('/register')
    else:
        # ENG: Redirect if user already has a session
        # TR: Kullanıcının halihazırda bir oturumu açık ise yönlendir
        if "user_id" in session:
            flash("You are already logged in.")
            return redirect("/")
        
        return render_template("register.html")

# ENG: Login route
# TR: Giriş yapma rotası
@mainbp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # ENG: User session check
        # TR: Kullanıcı oturum kontrolü
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
        
        # EN: Match the data with database
        # TR: Verileri veritabanı ile eşleştir
        user = DataBase.execute("SELECT users.id, users.username, users.password, users.name, roles.role FROM users JOIN roles ON users.id = roles.user_id WHERE username = ?", username)
        if not user or not check_password_hash(user[0]["password"], password):
            flash("Invalid username/password.")
            return redirect("/login")
        
        # EN: If login is successful, save the user information into the session
        # TR: Giriş başarılıysa bilgileri session'a kaydet
        session["user_id"] = user[0]["id"]
        session["username"] = user[0]["username"]
        session["name"] = user[0]["name"]
        session["role"] = user[0]["role"]
        return redirect(url_for('main.homepage'))
        
    else:
        # ENG: Check current session
        # TR: Mevcut oturum kontrolü
        if "user_id" in session:
            flash("You are already logged in.")
            return redirect("/")
        
        return render_template("login.html")


# ENG: Logout route
# TR: Oturum sonlandırma rotası
@mainbp.route("/logout")
def logout():
    
    # EN: Check session
    # TR: Oturum kontrolü
    if not "user_id" in session:
        flash("You are already logged out.")
        return redirect("/")
    
    # EN: Clear session if it exists
    # TR: Oturum mevcutsa session temizliği
    else:
        session.clear()
        flash("You have successfully logged out.")
        return redirect("/")
    

@mainbp.route('/visa')
def about_visa():
    return render_template('visa.html')


@mainbp.route('/greencard')
def about_greencard():
    return render_template('greencard.html')