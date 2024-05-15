from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from . import models, views

app = Flask(__name__)
app.config.from_object('config.Config')

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Неоходимо авторизоваться'
login_manager.login_message_category = 'alert-warning'

db.create_all()
