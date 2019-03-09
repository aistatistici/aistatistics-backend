from src import db


class Dataset(db.Model):

    """
        Dataset table
    """
    __tablename__ = "dataset"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    file_path = db.Column(db.String(264), unique=True, nullable=False)

    def __init__(self, name, file_path):
        self.name = name
        self.file_path = file_path

    def __repr__(self):
        return f"<Dataset {self.name}>"

    

