import json

from flask import request
from flask_restplus import Namespace, Resource
from keras.engine.saving import load_model

from ml.utils import process_data, ignore
from ml.utils.csv import open_csv_as_data_frame
from ml.utils.model import split_data, get_nr_features, dataset_to_time_series, generate_model, train_model, \
    render_history_graph, predict, render_predictions
from src import db
from .models import DataSet
from .parsers import dataset_parser
from .serializers import dataset_schema
from .utils import upload_file_location
import keras.backend as K

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
        dataset = DataSet(name=args['title'], file_path=destination, column_info=column_info)
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


@api.route('/split-dataset/<int:id>')
@api.param('id', 'The task identifier')
class SplitView(Resource):

    @api.doc("post_split")
    def post(self, id):
        data = json.loads(request.data)
        dataset = DataSet.query.get(id)
        column_info = dataset.column_info
        date_columns = []
        if column_info:
            date_columns = [
                c for c, v in column_info.items() if v.get('is_date', False)
            ]
        csv = open_csv_as_data_frame(dataset.file_path, date_columns=date_columns)
        subsets = process_data(csv, data['split'], data['augment'], data['process'], data['unique'],
                               data.get('ignore', []))

        for t, (s, column_extra_info) in subsets:
            extra = "_".join([k + "_" + str(d) for k, d in t.items()])
            name = dataset.name + "_" + extra
            col_info = dict(**column_info, **column_extra_info)
            for i in data.get('ignore', []):
                if column_info.get(i, None):
                    del column_info[i]
            destination = upload_file_location(name + ".csv", 'data/')
            s.to_csv(destination)
            ds = DataSet(name=name, file_path=destination, column_info=col_info)
            db.session.add(ds)
            db.session.commit()


@api.route('/train-dataset/<int:id>')
@api.param('id', 'The task identifier')
class TrainView(Resource):

    @api.doc("post_train")
    def post(self, id):
        data = json.loads(request.data)
        dataset = DataSet.query.get(id)
        column_info = dataset.column_info
        date_columns = []
        if column_info:
            date_columns = [
                c for c, v in column_info.items() if v.get('is_date', False)
            ]
        csv = ignore(open_csv_as_data_frame(dataset.file_path, date_columns=date_columns), data.get('ignore', []))
        n_out_columns = data['output']
        n_in = data['time_series_lag']

        ts = dataset_to_time_series(csv, n_in, 1, n_out_columns)
        print(ts)
        (train_X, train_y), (test_X, test_y) = split_data(ts, get_nr_features(csv), n_in, 1, n_out_columns)
        model = generate_model(get_nr_features(csv), n_in, 1, n_out_columns)

        history = train_model(model, train_X, train_y, test_X, test_y, data.get('epochs', 100))

        destination = upload_file_location(dataset.name + ".h5", 'models/')
        model.save(destination)
        dataset.model_path = destination
        dataset.train_info = data
        db.session.add(dataset)
        db.session.commit()
        K.clear_session()
        return render_history_graph(history)


@api.route('/predict-dataset/<int:id>')
@api.param('id', 'The task identifier')
class PredictView(Resource):

    @api.doc("post_predict")
    def post(self, id):
        dataset = DataSet.query.get(id)
        data = dataset.train_info
        column_info = dataset.column_info
        date_columns = []
        if column_info:
            date_columns = [
                c for c, v in column_info.items() if v.get('is_date', False)
            ]
        csv = ignore(open_csv_as_data_frame(dataset.file_path, date_columns=date_columns), data.get('ignore', []))
        n_out_columns = data['output']
        n_in = data['time_series_lag']
        ts = dataset_to_time_series(csv, n_in, 1, n_out_columns)
        (train_X, train_y), (test_X, test_y) = split_data(ts, get_nr_features(csv), n_in, 1, n_out_columns)
        model = load_model(dataset.model_path)

        preds = predict(model, test_X, get_nr_features(csv), n_in, with_ground_truth=False)

        destination = upload_file_location(dataset.name + ".h5", 'models/')
        model.save(destination)
        dataset.model_path = destination
        db.session.add(dataset)
        db.session.commit()
        K.clear_session()
        return render_predictions(preds, test_y)
