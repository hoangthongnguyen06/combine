from app import db
from datetime import datetime

class Post(db.Model):
    __tablename__ = 'TCTT_Posts'

    id = db.Column(db.String, primary_key=True)
    account_id = db.Column(db.String, db.ForeignKey('TCTT_Target.id'), nullable=False)
    nuance = db.Column(db.String, nullable=False, default='General')
    post_time = db.Column(db.TIMESTAMP(timezone=True), default=datetime.utcnow, nullable=False)
    created_at = db.Column(db.TIMESTAMP(timezone=True), default=datetime.utcnow, nullable=False)
    content = db.Column(db.String, nullable=False)
    likes = db.Column(db.Integer, default=0)
    comments = db.Column(db.Integer, default=0)
    shares = db.Column(db.Integer, default=0)
    platform = db.Column(db.String, nullable=False)
    link = db.Column(db.String, nullable=True)
    type = db.Column(db.String, nullable=False, default='Post')
    description = db.Column(db.String, nullable=True)

    # Define relationships if necessary
    # target = db.relationship('Target', back_populates='posts')

    def serialize(self):
        return {
            'id': self.id,
            'account_id': self.account_id,
            'nuance': self.nuance,
            'post_time': self.post_time.isoformat() if self.post_time else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'content': self.content,
            'likes': self.likes,
            'comments': self.comments,
            'shares': self.shares,
            'platform': self.platform,
            'link': self.link,
            'type': self.type,
            'description': self.description
        }
