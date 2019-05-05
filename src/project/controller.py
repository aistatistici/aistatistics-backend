from datetime import datetime

from flask import request
from flask_restplus import Namespace, Resource

from src import db
from .models import Project
from .parsers import project_parser
from .serializers import project_schema

api = Namespace('project', description="Project View Endpoint")


@api.route('/project/<int:id>')
@api.param('id', 'The Project identifier')
class ProjectView(Resource):

    @api.doc("Get method functionality for Project")
    def get(self, id):
        project = Project.query.get(id)
        if project:
            return project_parser.dump(project)

    @api.doc("Delete method functionality for Project")
    def delete(self, id):
        project = Project.query.get(id)
        if project:
            db.session.delete(project)
            db.session.commit()


@api.route('/project/')
class PostProjectView(Resource):

    @api.expect(project_parser)
    @api.doc("Post method functionality for Project")
    def post(self):
        args = project_parser.parse_args()
        project = Project(name=args['title'], description=args['description'], last_update=datetime.utcnow)
        db.session.add(project)
        db.session.commit()

        return project.id, 200

