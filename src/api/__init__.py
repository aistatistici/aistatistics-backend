from flask import Blueprint
from flask_restplus import Api


blueprint = Blueprint('file', __name__, url_prefix='/api')
api = Api(blueprint)

from .controller import api as file_namespace
api.add_namespace(file_namespace, path='/file')