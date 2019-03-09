from flask.json import jsonify
from flask_restplus import Namespace, Resource, fields, abort

from .parsers import file_upload
from .utils import upload_file_location

api = Namespace('file', description="Document parser for data entires")


@api.route('/upload-data-document')
class FileUpload(Resource):
    @api.expect(file_upload)
    def post(self):
        args = file_upload.parse_args()
        print(args['csv_file'])
        if args['csv_file'].mimetype == 'application/csv':
            destination = upload_file_location()
            args['csv_file'].save(destination)
        else:
            abort(400, 'The file needs to be ')
        return jsonify({'status', 'Done'})


@api.route('/get-data-document')
class File(Resource):

    def get(self):
        return jsonify({'message': 'In works'})
