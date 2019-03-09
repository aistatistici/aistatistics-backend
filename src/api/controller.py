from flask.json import jsonify
from flask_restplus import Namespace, Resource, fields, abort

from .parsers import file_upload
from .utils import upload_file_location

api = Namespace('file', description="Document parser for data entires")


@api.route('/upload-data-document')
@api.doc(id="upload", description="Uploads file")
class FileUpload(Resource):

    @api.expect(file_upload)
    def post(self):
        args = file_upload.parse_args()
        csv_file = args['file']
        if csv_file.mimetype == 'text/csv':
            destination = upload_file_location(csv_file.filename)
            csv_file.save(destination)
        else:
            abort(400, 'The file type needs to be a CSV')
        return 'Done', 200


@api.route('/get-data-document')
@api.doc('get_data_document')
class File(Resource):

    def get(self):
        return jsonify({'message': 'In works'})
