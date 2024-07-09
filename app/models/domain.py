# app/models/domain.py
from app import db

class Domain(db.Model):
    __tablename__ = 'domains'
    domain_id = db.Column(db.Integer, primary_key=True)
    domain_name = db.Column(db.String)

    posts = db.relationship("Post", back_populates="domain")
