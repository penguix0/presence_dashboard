from datetime import *
from flask import Flask

## Create an app object
app = Flask(__name__)
## Create config
app.config.from_pyfile('../config.py')

## --- Database --- ##
from flask_sqlalchemy import SQLAlchemy
db_path = "./database/presence.db"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True


db = SQLAlchemy(app)

from flask_login import UserMixin

class Organisation(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(40), nullable=False, default="default.jpg")
    password = db.Column(db.String(60), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    employees = db.relationship("Employee", backref="employer")
    settings = db.relationship("Settings", backref="organisation", lazy=True)

    ## When this object is printed
    def __repr__(self):
        return f"Organisation('{self.username}', '{self.email}', '{self.image_file}', '{self.settings}')"

class Settings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    loginMessage = db.Column(db.String(120), unique=False, nullable=False)
    logoutMessage = db.Column(db.String(120), unique=False, nullable=False)
    messageTime = db.Column(db.Float)
    organisation_id = db.Column(db.Integer, db.ForeignKey('organisation.id'), nullable=False)
    
    # ## Colors
    # primary_color = db.Column(db.String(6))
    # secondary_color = db.Column(db.String(6))
    # white_color = db.Column(db.String(6))
    # text_color = db.Column(db.String(6))


    ## When this object is printed
    def __repr__(self):
        return f"Settings('{self.id}', '{self.loginMessage}', '{self.logoutMessage}', '{self.messageTime}', '{self.organisation_id}')"

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), unique=False, nullable=False)
    last_name = db.Column(db.String(20), unique=False, nullable=False)
    present = db.Column(db.Boolean, nullable=False, default=False)
    organisation_id = db.Column(db.Integer, db.ForeignKey('organisation.id'), nullable=False)
    ## When this object is printed 
    def __repr__(self):
        return f"Employee('{self.first_name}', '{self.last_name}', '{self.present}')"

## Initialize database to prevent some errors
db.create_all()

## --- Database ---
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

## Protection against CSRF attacks when posting the button values
from flask_wtf.csrf import CSRFProtect

## Create and initialize the csrf protection
csrf = CSRFProtect(app)
csrf.init_app(app)

from flask_login import LoginManager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

from .views import dashboard, instellingen, login 