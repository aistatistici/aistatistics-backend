import pandas as pd
import json

from marshmallow import Schema, fields, INCLUDE

from .models import DataSet


class DatasetSchema(Schema):

    id = fields.Integer(required=True)
    name = fields.Str(required=True)
    data = fields.Method('get_data')

    def get_data(self, obj):
        data = pd.read_csv(obj.file_path)
        return {
            'columns': data.columns.values.tolist(),
            'data': data.values.transpose().tolist()
        }

    class Meta:

        unknown = INCLUDE


dataset_schema = DatasetSchema()
