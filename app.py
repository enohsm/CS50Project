from flask import Flask, session
from routes.main_routes import mainbp
from routes.greencard_routes import gcbp
from routes.visa_routes import visabp
from routes.profile_routes import profilebp


app = Flask(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = True
app.jinja_env.auto_reload = True

# EN: I'm handling the login status in the template
# TR: Giriş kontrolünü template'e aktarıyorum
@app.context_processor
def logged_in():
    return dict(
        logged_in = ("user_id" in session),
        username = session.get("username", "Guest")
        )


# EN: Registering blueprints for the routes
# TR: Rotalar için modülleri ekliyorum
app.register_blueprint(mainbp)
app.register_blueprint(gcbp)
app.register_blueprint(visabp)
app.register_blueprint(profilebp)