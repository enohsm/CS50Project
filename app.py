from flask import Flask, session
from routes.main_routes import mainbp
from routes.request_routes import requestbp
from routes.profile_routes import profilebp
from routes.dashboard_routes import dbbp


app = Flask(__name__)
app.secret_key = b"C_Szotu9soz_-01.,01Qsxn72hjsk_."

app.config["TEMPLATES_AUTO_RELOAD"] = True
app.jinja_env.auto_reload = True

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


# EN: Registering blueprints for the routes
# TR: Rotalar için modülleri ekliyorum
app.register_blueprint(mainbp)
app.register_blueprint(requestbp)
app.register_blueprint(profilebp)
app.register_blueprint(dbbp)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)