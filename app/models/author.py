# app/models/author.py
from app import db

class Author(db.Model):
    __tablename__ = 'authors'
    author_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    sex = db.Column(db.String)
    birthdate = db.Column(db.Date)
    unit_id = db.Column(db.Integer, db.ForeignKey('units.unit_id'))
    domain_id = db.Column(db.Integer, db.ForeignKey('domains.domain_id'))

    unit = db.relationship("Unit", back_populates="authors")
    domain = db.relationship("Domain", back_populates="authors")
