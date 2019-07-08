import os
from sqla_wrapper import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, length

db = SQLAlchemy(os.getenv("DATABASE_URL", "sqlite:///localhost.sqlite"))  # this connects to a database either on Heroku or on localhost


class Loginform(FlaskForm):
    name = StringField("username", validators=[InputRequired, length(min=4, max=15)])
    password = PasswordField("password", validators=[InputRequired, length(min=8, max=80)])
    remember = BooleanField("rememberme")



