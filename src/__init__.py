import os

from flask import Flask
from flask_script import Manager
from flask_pymongo import PyMongo
from flask_marshmallow import Marshmallow

from src.config import config_dict
from .api import blueprint as api

app = Flask(__name__)
app.config.from_object(config_dict[os.getenv('ENVIRONEMENT', 'development')])
app.register_blueprint(api, url_prefix='/api')

manager = Manager(app)
mongo = PyMongo(app)
ma = Marshmallow(app)
