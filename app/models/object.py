# app/models/object.py
from app import db
from datetime import datetime

class Object(db.Model):
    __tablename__ = 'objects'
    
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, nullable=False)
    keys = db.Column(db.String, nullable=True)
    address = db.Column(db.String, nullable=True)
    province = db.Column(db.Integer, nullable=True)
    district = db.Column(db.Integer, nullable=True)
    ward = db.Column(db.Integer, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    latitude = db.Column(db.Float, nullable=True)
    status = db.Column(db.String, nullable=False, default='Active')
    type = db.Column(db.String, nullable=False)
    date = db.Column(db.Date, default=datetime)
