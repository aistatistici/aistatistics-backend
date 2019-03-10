from flask_restplus import Namespace, Resource

from src import db
from .models import DataSet
from .parsers import dataset_parser
from .serializers import dataset_schema
from .utils import upload_file_location

api = Namespace('file', description="Document parser for data entires")


@api.route('/upload-data-document')
@api.doc(id="upload", description="Uploads file")
class FileUpload(Resource):

    @api.expect(dataset_parser)
    def post(self):
        args = dataset_parser.parse_args()
        csv_file = args['file']
        date_fields = args.get('date_fields', []) or []
        if not isinstance(date_fields, list):
            date_fields = [date_fields]
        column_info = {}

        for d in date_fields:
            column_info[d] = {
                "is_date": True
            }

        destination = upload_file_location(csv_file.filename, 'data/')
        csv_file.save(destination)
        dataset = DataSet(name=args['name'], file_path=destination, column_info=column_info)
        db.session.add(dataset)
        db.session.commit()

        return dataset.id, 200


@api.route('/get-dataset/<int:id>')
@api.param('id', 'The task identifier')
class DataSetView(Resource):

    @api.doc("get_dataset")
    def get(self, id):
        dataset = DataSet.query.get(id)
        if dataset:
            return dataset_schema.dump(dataset)

    @api.doc("delete_dataset")
    @api.response(204, "Dataset deleted")
    def delete(self, id):
        pass
