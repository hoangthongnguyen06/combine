# app/models/nuance.py
from app import db

class Nuance(db.Model):
    __tablename__ = 'nuances'
    nuance_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    posts = db.relationship("Post", back_populates="nuance")
