from typing import Text
from sqlalchemy.dialects.postgresql import JSON

from src import db


class DataSet(db.Model):

    """
        Dataset table
    """
    __tablename__ = "dataset"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(264), unique=True, nullable=False)
    model_path = db.Column(db.String(264), unique=True, nullable=True)
    column_info = db.Column(JSON, nullable=True)
    train_info = db.Column(JSON, nullable=True)

    def __init__(self, name=None, file_path=None, column_info=None):
        self.name = name
        self.file_path = file_path
        self.column_info = column_info

    def __repr__(self):
        return f"<Dataset {self.name}>"



