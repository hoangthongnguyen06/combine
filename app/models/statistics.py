from app import db
from datetime import datetime

class Statistics(db.Model):
    __tablename__ = 'TCTT_Statistics'

    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(100), nullable=False)
    total_count = db.Column(db.Integer, nullable=False)
    positive_count = db.Column(db.Integer, nullable=False)
    neutral_count = db.Column(db.Integer, nullable=False)
    negative_count = db.Column(db.Integer, nullable=False)
    added_to_json = db.Column(db.String, default="1")
    # date = db.Column(db.Date, default=datetime.utcnow)
    # created_at = db.Column(db.TIMESTAMP(timezone=True), default=datetime.utcnow)
    #created_at = db.Column(db.TIMESTAMP(timezone=True), default=datetime.utcnow, nullable=False)

    def __init__(self, id, location, total_count, positive_count, neutral_count, negative_count, added_to_json):
        self.id = id
        self.location = location
        self.total_count = total_count
        self.positive_count = positive_count
        self.neutral_count = neutral_count
        self.negative_count = negative_count
        self.added_to_json = added_to_json

    def __repr__(self):
        return f'<Statistics {self.location}>'