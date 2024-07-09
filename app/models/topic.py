# app/models/topic.py
from app import db

class Topic(db.Model):
    __tablename__ = 'topics'
    topic_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    keys = db.Column(db.String)

    posts = db.relationship("Post", back_populates="topic")
