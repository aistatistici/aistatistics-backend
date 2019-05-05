import os
import sys

BASE_DIR = os.path.dirname(__name__)

sys.path.append(os.path.join(BASE_DIR, '..'))

from flask import Flask
from flask_script import Manager
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from flask_migrate import Migrate, MigrateCommand
from flask_sqlalchemy import SQLAlchemy

from .config import config_dict

app = Flask(__name__)
app.config.from_object(config_dict[os.getenv('ENVIRONEMENT', 'development')])

cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

db = SQLAlchemy(app)


from .api import blueprint as api
from .project import blueprint as project_app
app.register_blueprint(api, url_prefix='/api')
app.register_blueprint(project_app, url_prefix='/api')

migrate = Migrate(app, db)
manager = Manager(app)
ma = Marshmallow(app)


@manager.command
def run():
    app.run(host='0.0.0.0')


manager.add_command('db', MigrateCommand)