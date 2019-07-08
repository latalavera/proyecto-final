from flask import Flask, render_template, request, make_response, redirect, url_for
from models import Loginform
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.config["SECRET_KEY"] = "1234567890"

@app.route("/")
def index():
    return (render_template("index.html"))


@app.route("/login")
def login():
    form = Loginform()
    return (render_template("login.html"))


@app.route("/signup")
def signup():
    return (render_template("signup.html"))


@app.route("/dashboard")
def dashboard():
    return (render_template("dashboard.html"))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)


