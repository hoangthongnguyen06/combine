from datetime import datetime
from app import db

class Topic_new(db.Model):
    __tablename__ = 'TCTT_Chude'

    uid = db.Column(db.String, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    parent_id = db.Column(db.String)
    parent_name = db.Column(db.String)
    status = db.Column(db.String(20), default='Active')
    asign = db.Column(db.String(20))
    system = db.Column(db.String)

    @classmethod
    def create(cls, uid, name, parent_id=None, parent_name=None, status='Active', asign=None, system=None):
        topic = cls(
            uid=uid,
            name=name,
            parent_id=parent_id,
            parent_name=parent_name,
            status=status,
            asign=asign,
            system=system
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
    def get_by_id(cls, uid):
        return cls.query.get(uid)

    def serialize(self):
        return {
            'uid': self.uid,
            'name': self.name,
            'parent_id': self.parent_id,
            'parent_name': self.parent_name,
            'status': self.status,
            'asign': self.asign,
            'system': self.system
        }
