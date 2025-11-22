from flask import Flask, session
from flask_mail import Mail
from datetime import datetime
from routes.main_routes import mainbp
from routes.request_routes import requestbp
from routes.profile_routes import profilebp
from routes.dashboard_routes import dbbp
from routes.admin_db_routes import adminbp


app = Flask(__name__)
app.secret_key = b"C_Szotu9soz_-01.,01Qsxn72hjsk_."

app.config["TEMPLATES_AUTO_RELOAD"] = True
app.jinja_env.auto_reload = True

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'xaharsystem@gmail.com'
app.config['MAIL_PASSWORD'] = 'xaharsystem22'
app.config['MAIL_DEFAULT_SENDER'] = 'xaharsystem@gmail.com'

# EN: I'm handling the login status in the template
# TR: Giriş kontrolünü template'e aktarıyorum
@app.context_processor
def logged_in():
    return dict(
        logged_in = ("user_id" in session),
        user__username = session.get("username", "Guest"),
        user__name = session.get("name"),
        user__role = session.get("role")
        )

@app.template_filter('format_date')
def format_date(date):
    return datetime.strptime(date, '%Y-%m-%d %H:%M:%S').strftime('%d/%m/%Y - %H:%M:%S')

@app.template_filter('input_date')
def input_date(date):
    return datetime.strptime(date, '%d/%m/%Y').strftime('%Y-%m-%d')


# EN: Registering blueprints for the routes
# TR: Rotalar için modülleri ekliyorum
app.register_blueprint(mainbp)
app.register_blueprint(requestbp)
app.register_blueprint(profilebp)
app.register_blueprint(dbbp)
app.register_blueprint(adminbp)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)