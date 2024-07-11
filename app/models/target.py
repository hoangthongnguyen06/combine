# app/models/target.py
from app import db
from datetime import datetime

class Target(db.Model):
    __tablename__ = 'targets'
    
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, nullable=False)
    sex = db.Column(db.String, nullable=True)
    birthday = db.Column(db.Date, nullable=True)
    status = db.Column(db.String, nullable=False, default='Active')
    state = db.Column(db.String, nullable=False, default='Positive')
    type = db.Column(db.String, nullable=False, default='Individual')
    domain = db.Column(db.String, nullable=False)
    date = db.Column(db.Date, default=datetime)

    @classmethod
    def create(cls, name, sex=None, birthday=None, state=None, type=None, domain=None):
        target = cls(
            name=name,
            sex=sex,
            birthday=birthday,
            state=state,
            type=type,
            domain=domain
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
            'date': self.date.isoformat()
        }