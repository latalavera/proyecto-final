import os
import datetime
from sqla_wrapper import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SelectField
from wtforms.validators import InputRequired, Email, Length
from flask_login import UserMixin
from wtforms.fields.html5 import EmailField


db = SQLAlchemy(os.getenv("DATABASE_URL", "sqlite:///localhost.sqlite"))  # this connects to a database either on Heroku or on localhost


class User(UserMixin, db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))
    city = db.Column(db.String(20))


class Mensaje(db.Model, UserMixin):
    __tablename__ = "mensaje"
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String)
    message = db.Column(db.Text)
    receiver = db.Column(db.String, db.ForeignKey("user.email"))
    sender = db.Column(db.String, db.ForeignKey("user.email"))
    read = db.Column(db.Boolean, default=False)
    date = db.Column(db.DateTime, default=datetime.datetime.now)


class Loginform(FlaskForm):
    name = StringField("username", validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField("password", validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField("remember me")


class Registerform(FlaskForm):
    name = StringField("username", validators=[InputRequired(), Length(min=4, max=15)])
    email = StringField("email", validators=[InputRequired(), Length(min=4, max=50)])
    password = PasswordField("password", validators=[InputRequired(), Length(min=8, max=80)])
    city = StringField("city", validators=[InputRequired(), Length(min=4, max=20)])


def get_choices(my_user):
    users = db.query(User).all()
    return [(user.email, user.email) for user in users if user.email != my_user.email]


class Messageform(FlaskForm):
    subject = StringField("Subject", validators=[InputRequired(), Length(min=4, max=500)])
    message = StringField("Message", validators=[InputRequired(), Length(min=4, max=500)])
    receiver_email = SelectField("Receiver email", validators=[InputRequired(), Email("Introduce a valid email address"), Length(min=4, max=50)])
