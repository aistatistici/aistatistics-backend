import werkzeug

from flask_restplus import reqparse

file_upload = reqparse.RequestParser()
file_upload.add_argument('csv', type=werkzeug.datastructures.FileStorage,
                         location='file',
                         required=True,
                         help='CSV file')
