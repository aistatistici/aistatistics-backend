
from marshmallow import Schema, fields, INCLUDE


class ProjectSchema(Schema):

    id = fields.Integer(required=True)
    name = fields.Str(required=True)
    description = fields.Str(required=True)
    last_update = fields.Str(required=False)


project_schema = ProjectSchema()

