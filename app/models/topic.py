# app/models/topic.py
from app import db
from datetime import datetime

class Topic(db.Model):
    __tablename__ = 'topics'
    
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, nullable=False)
    parent_id = db.Column(db.String, nullable=True)
    status = db.Column(db.String, nullable=False, default='Active')
    state = db.Column(db.String, nullable=True)
    date = db.Column(db.Date, default=datetime)
