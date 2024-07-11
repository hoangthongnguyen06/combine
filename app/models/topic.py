from datetime import datetime
from app import db

class Topic(db.Model):
    __tablename__ = 'topics'

    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    parent_id = db.Column(db.String)
    status = db.Column(db.String(20), default='Active')
    state = db.Column(db.String(20))
    date = db.Column(db.Date, default=datetime.utcnow)

    @classmethod
    def create(cls, name, parent_id=None, status='Active', state=None):
        topic = cls(
            name=name,
            parent_id=parent_id,
            status=status,
            state=state
        )
        db.session.add(topic)
        db.session.commit()
        return topic

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
            'name': self.name,
            'parent_id': self.parent_id,
            'status': self.status,
            'state': self.state,
            'date': self.date.isoformat()
        }