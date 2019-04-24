from datetime import datetime

from src import db

class Project(db.Model):

    __tablename__ = "project"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    last_update = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, name=None, description=None, last_update=None):
        self.name = name
        self.description = description
        self.last_update = last_update

    def __repr__(self):
        return f"<Project {self.name}>"


