# Import stuff
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


# Define the WSGI application object
app = Flask(__name__)

login_manager = LoginManager()

# Configurations
app.config.from_object('config')

# Bcrypt
bcrypt = Bcrypt(app)

# Create db object
db = SQLAlchemy(app)

# load sk
sk_pem = open('sk.pem').read()

# Build the database:
# This will create the database file using SQLAlchemy
# and lets go
from . import model, views
