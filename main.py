from flask import Flask, render_template, redirect, url_for, request, make_response
from models import Loginform, Registerform, User, Mensaje, db, Messageform, get_choices
from flask_login import login_required, logout_user, LoginManager, login_user, current_user
from flask_bootstrap import Bootstrap
from werkzeug.security import generate_password_hash, check_password_hash       #security features for the password
#from flask_socketio import SocketIO, send


app = Flask(__name__)
db.create_all()
app.config["SECRET_KEY"] = "1234567890"
Bootstrap(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    return db.query(User).get(int(user_id))


@app.route("/")
def index():
    return render_template("index.html", current_user=current_user)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = Loginform()
    if form.validate_on_submit():
        user = db.query(User).filter_by(name=form.name.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):  #this function automatically compares the 2 passwords (user.password and form.password)
                login_user(user, remember=form.remember.data)
                return redirect(url_for("dashboard"))
        return "Invalid username or password"
    return render_template("login.html", form=form, current_user=current_user)


@app.route("/signup", methods=["GET", "POST"])
def signup():
    form = Registerform()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method="sha256")   #this generates a 80 character long password
        new_user = User(name=form.name.data, email=form.email.data, password=hashed_password, city=form.city.data)
        db.add(new_user)
        db.commit()
        return redirect(url_for("login"))
    return render_template("signup.html", form=form, current_user=current_user)


@app.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    form = Messageform()
    form.receiver_email.choices = get_choices(current_user)
    if request.method == "GET":
        messages = db.query(Mensaje).filter_by(receiver=current_user.email, read=False).all()
        users = db.query(User).all()
        return render_template("dashboard.html", messages=messages, form=form, current_user=current_user, users=users)

    else:
        if form.validate_on_submit():
            msg = Mensaje(subject=form.subject.data, message=form.message.data, receiver=form.receiver_email.data,
                          sender=current_user.email, read=False)
            db.add(msg)
            db.commit()
            data = "Your message has been sent"
            return render_template("dashboard.html", data=data, form=form, current_user=current_user, msg=msg)
        else:
            data = "Error, review the entered data"
            return render_template("dashboard.html", data=data, form=form, current_user=current_user)


@app.route('/messages')
@app.route('/messages/<msg_id>')
@login_required
def message_details(msg_id=None):
    if msg_id:
        msg = db.query(Mensaje).get(int(msg_id))

        if msg and msg.receiver==current_user.email:
            msg.read = True
            db.add(msg)
            db.commit()

            return render_template("messages.html", current_msg=msg, current_user=current_user)
        else:
            return "Message ID not valid!"
    else:
        messages = list(db.query(Mensaje).filter_by(receiver=current_user.email))

        messages.sort(key=lambda s: s.date)

        read = list(filter(lambda s: s.read, messages))
        non_read = list(filter(lambda s: not s.read, messages))

        for msg in non_read:
            msg.read = True
            db.add(msg)
            db.commit()

        return render_template("messages.html", msg_read=read, msg_non_read=non_read, current_user=current_user)

    return render_template("messages.html", no_msg=True)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True, port=8000)


