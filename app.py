from flask import Flask, session
from flask_mail import Mail
from datetime import datetime
from routes.main_routes import mainbp
from routes.request_routes import requestbp
from routes.profile_routes import profilebp
from routes.dashboard_routes import dbbp
from routes.admin_db_routes import adminbp


app = Flask(__name__)

# ENG: Secret key for session signing
# TR: Oturum imzalama için SECRET_KEY
app.secret_key = b"C_Szotu9soz_-01.,01Qsxn72hjsk_.12aodfpr0a9svcj__!?srpt"

app.config["TEMPLATES_AUTO_RELOAD"] = True
app.jinja_env.auto_reload = True

# ENG: Mail settings
# TR: Mail ayarları
mail = Mail()

app.config['MAIL_SERVER'] = 'sandbox.smtp.mailtrap.io'
app.config['MAIL_PORT'] = 2525
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'setmailsetting'
app.config['MAIL_PASSWORD'] = 'setmailsetting'
app.config['MAIL_DEFAULT_SENDER'] = 'setmailsetting'

mail.init_app(app)

# ENG: I'm handling the login status in the template
# TR: Giriş kontrolünü template'e aktarıyorum
@app.context_processor
def logged_in():
    return dict(
        logged_in = ("user_id" in session),
        user__username = session.get("username"),
        user__name = session.get("name"),
        user__role = session.get("role")
        )

# ENG: Jinja filter to format date as YYYY/MM/DD
# TR: Tarihi YYYY/MM/DD şeklinde biçimlendirecek jinja filtresi 
@app.template_filter('format_date')
def format_date(date):
    return datetime.strptime(date, '%Y-%m-%d %H:%M:%S').strftime('%d/%m/%Y - %H:%M:%S')

# ENG: Jinja filter to secure identity number
# TR: Kimlik numarasını güvenli şekilde biçimlendirme
@app.template_filter('secure_identity')
def secure_identity(identity):
    masked_ident = identity[:3] + '*****' + identity[9:]
    return masked_ident

# ENG: Jinja filter to secure contact number
# TR: İletişim numarasını güvenli şekilde biçimlendirme
@app.template_filter('secure_contact')
def secure_contact(contact):
    masked_contact = ('*'* len(contact[:7])) + contact[7:]
    return masked_contact

# ENG: Jinja filter to format date as DD/MM/YYYY
# TR: Tarihi DD/MM/YYYY şeklinde biçimlendiren jinja filtresi
@app.template_filter('input_date')
def input_date(date):
    return datetime.strptime(date, '%d/%m/%Y').strftime('%Y-%m-%d')


# ENG: Registering blueprints for the routes
# TR: Rotalar için modülleri ekliyorum
app.register_blueprint(mainbp)
app.register_blueprint(requestbp)
app.register_blueprint(profilebp)
app.register_blueprint(dbbp)
app.register_blueprint(adminbp)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)