from flask_restplus import reqparse


project_parser = reqparse.RequestParser()
project_parser.add_argument('name',
                            required=True,
                            help='Project Name')
project_parser.add_argument('description',
                            required=True,
                            help='Project Description')

