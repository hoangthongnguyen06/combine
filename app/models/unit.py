# app/models/unit.py
from app import db

class Unit(db.Model):
    __tablename__ = 'units'
    unit_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    authors = db.relationship("Author", back_populates="unit")
