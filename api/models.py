from pensieve import db
from sqlalchemy.dialects.postgresql import JSON


class Run(db.Model):
    __tablename__ = 'runs'

    id = db.Column(db.Integer, primary_key=True)

    def __init__(self):
        pass

    def __repr__(self):
        return '<id {}>'.format(self.id)
