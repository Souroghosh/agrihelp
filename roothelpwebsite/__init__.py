from logging import NullHandler
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# from flask_bcrypt import Bcrypt
# from flask_login import LoginManager


app = Flask(__name__)

app.config['SECRET_KEY'] = 'bbf34737e43416a1318538f507cb100e'

from roothelpwebsite import routes
