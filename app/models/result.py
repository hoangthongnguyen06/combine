# app/models/result.py
from app import db

class Result(db.Model):
    __tablename__ = 'results'
    
    id = db.Column(db.String, primary_key=True)
    account_id = db.Column(db.String, db.ForeignKey('targets.id'), nullable=False)
    post_id = db.Column(db.String, db.ForeignKey('posts.id'), nullable=False)
    bots_number = db.Column(db.Integer, nullable=False, default=0)
    completed_time = db.Column(db.Time, nullable=True)
    status = db.Column(db.String, nullable=False, default='Processing')
    type = db.Column(db.String, nullable=False, default='ProActive')

    target = db.relationship('Target', back_populates='results')
    post = db.relationship('Post', back_populates='results')
