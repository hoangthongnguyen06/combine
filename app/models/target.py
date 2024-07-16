# app/models/target.py
from app import db
from datetime import datetime

class Target(db.Model):
    __tablename__ = 'TCTT_Target'
    
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, nullable=False)
    gender = db.Column(db.String, nullable=True)
    status = db.Column(db.String, nullable=False, default='Active')
    state = db.Column(db.String, nullable=False, default='Positive')
    type = db.Column(db.String, nullable=False, default='Individual')
    platform = db.Column(db.String, nullable=False)
    created_at = db.Column(db.Date, default=datetime)
    uid = db.Column(db.String, nullable=False)
    region = db.Column(db.String, nullable=False)
    assign = db.Column(db.ARRAY(db.String), nullable=True, default=[])

    @classmethod
    def create(cls, name, sex=None, birthday=None, state=None, type=None, domain=None, assign=None):
        target = cls(
            name=name,
            sex=sex,
            birthday=birthday,
            state=state,
            type=type,
            domain=domain,
            assign=assign
        )
        db.session.add(target)
        db.session.commit()
        return target

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
            'sex': self.sex,
            'birthday': self.birthday.isoformat() if self.birthday else None,
            'status': self.status,
            'state': self.state,
            'type': self.type,
            'domain': self.domain,
            'assign': self.assign,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'uid': self.uid,
            'region': self.region
        }
