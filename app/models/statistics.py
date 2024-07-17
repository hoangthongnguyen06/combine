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
    #created_at = db.Column(db.TIMESTAMP(timezone=True), default=datetime.utcnow, nullable=False)

    def __init__(self, id, location, total_count, positive_count, neutral_count, negative_count):
        self.id = id
        self.location = location
        self.total_count = total_count
        self.positive_count = positive_count
        self.neutral_count = neutral_count
        self.negative_count = negative_count

    def __repr__(self):
        return f'<Statistics {self.location}>'