from datetime import datetime

from marshmallow import Schema, fields, INCLUDE

from ml.utils.csv import open_csv_as_data_frame


class DatasetSchema(Schema):
    id = fields.Integer(required=True)
    name = fields.Str(required=True)
    data = fields.Method('get_data')
    model_path = fields.Str(required=False)

    def get_data(self, obj):
        column_info = obj.column_info
        date_columns = []
        if column_info:
            date_columns = [
                c for c, v in column_info.items() if v.get('is_date', False)
            ]
        data = open_csv_as_data_frame(obj.file_path, date_columns=date_columns)

        def serialize_value(v):
            if isinstance(v, datetime):
                return v.isoformat()
            return v

        return {
            'columns': data.columns.values.tolist(),
            'data': [[serialize_value(d2) for d2 in d1] for d1 in data.values.transpose().tolist()]
        }

    class Meta:

        unknown = INCLUDE


dataset_schema = DatasetSchema()
