from flask import Blueprint
from flask_restplus import Api
from .controller import api as file_ns

blueprint = Blueprint('project', __name__)
api = Api(blueprint)

api.add_namespace(file_ns, path='/project')