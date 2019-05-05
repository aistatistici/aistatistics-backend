from flask import Blueprint
from flask_restplus import Api

blueprint = Blueprint('project', __name__ , url_prefix='/api/project')
api = Api(blueprint)


from .controller import api as project_namespace
api.add_namespace(project_namespace, path='/project')