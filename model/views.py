from rest_framework.decorators import api_view
from keras.engine.saving import load_model
import keras.backend as K
from utility.views import SerializerDispachViewSet


from ml.utils import process_data, ignore
from ml.utils.csv import open_csv_as_data_frame
from ml.utils.model import (split_data, get_nr_features, dataset_to_time_series, generate_model, train_model, \
                            render_history_graph, predict, render_predictions)

from .models import DataSet
from .filters import DataSetFilter
from .serializers import DataSetSerializer, PostDataSetSerializer


class DataSetView(SerializerDispachViewSet):

    queryset = DataSet.objects.all()
    serializer_class = DataSetSerializer
    serializer_action_classes = {
        'GET': DataSetSerializer,
        'POST': PostDataSetSerializer,
        'PATCH': PostDataSetSerializer,
    }
    filter_class = DataSetFilter


@api_view(['POST'])
def train_view(request, id):

    data = request.data
    dataset = DataSet.objects.get(id)
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
    # db.session.add(dataset)
    # db.session.commit()
    K.clear_session()
    return render_history_graph(history)


@api_view(['POST'])
def split_view(request, id):

    data = request.data
    dataset = DataSet.objects.get(id)
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
        s.to_csv(destination)
        ds = DataSet.objects.create(name=name, file_path=destination, column_info=col_info)
        ds.save()


@api_view(['POST'])
def predict_view(request, id):

    dataset = DataSet.objects.get(id)
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
    # db.session.add(dataset)
    # db.session.commit()
    K.clear_session()
    return render_predictions(preds, test_y)
