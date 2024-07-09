# app/models/post.py
from datetime import datetime
from app import db

class Post(db.Model):
    __tablename__ = 'posts'
    post_id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('authors.author_id'))
    nuance_id = db.Column(db.Integer, db.ForeignKey('nuances.nuance_id'))
    date = db.Column(db.DateTime, default=datetime.utcnow)
    content = db.Column(db.String)
    likes = db.Column(db.Integer)
    comments = db.Column(db.Integer)
    shares = db.Column(db.Integer)
    topic_id = db.Column(db.Integer, db.ForeignKey('topics.topic_id'))
    domain_id = db.Column(db.Integer, db.ForeignKey('domains.domain_id'))
    link = db.Column(db.String)
    hashtag = db.Column(db.String)

    author = db.relationship("Author", back_populates="posts")
    nuance = db.relationship("Nuance", back_populates="posts")
    topic = db.relationship("Topic", back_populates="posts")
    domain = db.relationship("Domain", back_populates="posts")
