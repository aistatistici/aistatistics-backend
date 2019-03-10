import pandas as pd
import json

from marshmallow import Schema, fields, INCLUDE

from .models import DataSet
from ml.utils.csv import open_csv_as_data_frame


class DatasetSchema(Schema):

    id = fields.Integer(required=True)
    name = fields.Str(required=True)
    data = fields.Method('get_data')

    def get_data(self, obj):
        column_info = obj.column_info
        date_columns = []
        if column_info:
            date_columns = [
                c for c, v in column_info.items() if v.get('is_date', False)
            ]
        data = open_csv_as_data_frame(obj.file_path, date_columns=date_columns)
        return {
            'columns': data.columns.values.tolist(),
            'data': data.values.transpose().tolist()
        }

    class Meta:

        unknown = INCLUDE


dataset_schema = DatasetSchema()
