from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Channel(db.Model):
    __tablename__ = 'TCTT_Channel'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    type = db.Column(db.Integer, nullable=False)
    url = db.Column(db.String(255), nullable=False)
    total_post = db.Column(db.Integer, nullable=False)
    created_by_id = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.TIMESTAMP(timezone=True), default=datetime.utcnow, nullable=False)

    def __init__(self, id, name, type, url, total_post, created_by_id, created_at):
        self.id = id
        self.name = name
        self.type = type
        self.url = url
        self.total_post = total_post
        self.created_by_id = created_by_id
        self.created_at = datetime.strptime(created_at, "%Y/%m/%d %H:%M:%S")

    def __repr__(self):
        return f'<Channel {self.name}>'

# Example of how to create the table
# db.create_all()
