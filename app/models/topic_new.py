from datetime import datetime
from app import db


class Topic_new(db.Model):
    __tablename__ = 'TCTT_Chude'

    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    parent_id = db.Column(db.String)
    parent_name = db.Column(db.String)
    status = db.Column(db.String(20), default='Active')
    assign = db.Column(db.String(20))
    system = db.Column(db.String)
    keyword = db.Column(ARRAY(db.String))
    created_at = db.Column(db.Date, default=datetime.utcnow)
    added_to_json = db.Column(db.String, default="1")

    @classmethod
    def create(cls, uid, name, keyword, created_at, parent_id=None, parent_name=None, status='Active', assign=None, system=None):
        topic = cls(
            id=uid,
            name=name,
            parent_id=parent_id,
            parent_name=parent_name,
            status=status,
            assign=assign,
            system=system,
            keyword=keyword,
            created_at=created_at
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
            'id': self.id,
            'name': self.name,
            'parent_id': self.parent_id,
            'parent_name': self.parent_name,
            'status': self.status,
            'assign': self.assign,
            'system': self.system,
            'keyword': self.keyword,
            'created_at': self.created_at
        }
