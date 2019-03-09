import os

from flask import Flask
from flask_script import Manager
from flask_pymongo import PyMongo
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from flask_migrate import Migrate, MigrateCommand
from flask_sqlalchemy import SQLAlchemy

from src.config import config_dict
from .api import blueprint as api

app = Flask(__name__)
app.config.from_object(config_dict[os.getenv('ENVIRONEMENT', 'development')])
app.register_blueprint(api, url_prefix='/api')

cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)
mongo = PyMongo(app)
ma = Marshmallow(app)


@manager.command
def run():
    app.run(host='0.0.0.0')


manager.add_command('db', MigrateCommand)