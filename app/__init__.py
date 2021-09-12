from config import Config
from flask import Flask, url_for
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
login=LoginManager(app)
login.login_view='patient_login' # specify the login page to redirect when require login

from app import routes,models

