from werkzeug.datastructures import FileStorage

from flask_restplus import reqparse

dataset_parser = reqparse.RequestParser()
dataset_parser.add_argument('file', type=FileStorage,
                            location='files',
                            required=True,
                            help='CSV file')
dataset_parser.add_argument('name',
                            required=True,
                            help='Name of the dataset')
