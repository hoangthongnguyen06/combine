# app/models/hashtag.py
from app import db

class Hashtag(db.Model):
    __tablename__ = 'hashtags'
    hashtag_id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String)
