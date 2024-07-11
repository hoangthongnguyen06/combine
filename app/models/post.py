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

    @classmethod
    def create(cls, account_id, content, domain, link=None, hashtag=None, description=None):
        post = cls(account_id=account_id, content=content, domain=domain, link=link, hashtag=hashtag, description=description)
        db.session.add(post)
        db.session.commit()
        return post

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_all(cls):
        return cls.query.all()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get(id)

    def serialize(self):
        return {
            'id': self.id,
            'account_id': self.account_id,
            'nuance_id': self.nuance_id,
            'date': self.date.isoformat(),
            'content': self.content,
            'likes': self.likes,
            'comments': self.comments,
            'shares': self.shares,
            'domain': self.domain,
            'link': self.link,
            'hashtag': self.hashtag,
            'type': self.type,
            'description': self.description
        }