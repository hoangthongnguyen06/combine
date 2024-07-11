# app/models/target.py
from app import db
from datetime import datetime

class Target(db.Model):
    __tablename__ = 'targets'
    
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, nullable=False)
    sex = db.Column(db.String, nullable=True)
    birthday = db.Column(db.Date, nullable=True)
    status = db.Column(db.String, nullable=False, default='Active')
    state = db.Column(db.String, nullable=False, default='Positive')
    type = db.Column(db.String, nullable=False, default='Individual')
    domain = db.Column(db.String, nullable=False)
    date = db.Column(db.Date, default=datetime)
