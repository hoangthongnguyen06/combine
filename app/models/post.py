# app/models/post.py
from app import db
from datetime import datetime

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.String, primary_key=True)
    account_id = db.Column(db.String, db.ForeignKey('targets.id'), nullable=False)
    nuance = db.Column(db.String, nullable=False, default='General')
    date = db.Column(db.Date, default=datetime.utcnow)
    content = db.Column(db.String, nullable=False)
    likes = db.Column(db.Integer, default=0)
    comments = db.Column(db.Integer, default=0)
    shares = db.Column(db.Integer, default=0)
    domain = db.Column(db.String, nullable=False)
    link = db.Column(db.String, nullable=True)
    hashtag = db.Column(db.String, nullable=True)
    type = db.Column(db.String, nullable=False, default='Post')
    description = db.Column(db.String, nullable=True)

    target = db.relationship('Target', back_populates='posts')
