from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Database
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
active_sessions = {}
max_active_sessions = 3

# Authentication
login_manager = LoginManager(app)
#string below is function name of route (same as used in the "url_for" function)
login_manager.login_view = 'users.login'
#replace the default flash message
login_manager.login_message = "Please log in to access this page!"
login_manager.login_message_category = "info"

from autoscrape import routes, models

db.create_all()
