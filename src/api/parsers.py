from flask_restplus import reqparse
from werkzeug.datastructures import FileStorage

dataset_parser = reqparse.RequestParser()
dataset_parser.add_argument('file', type=FileStorage,
                            location='files',
                            required=True,
                            help='CSV file')
dataset_parser.add_argument('name',
                            required=True,
                            help='Name of the dataset')
dataset_parser.add_argument('date_fields',
                            required=False,
                            help="Columns that need to be parsed as date")
