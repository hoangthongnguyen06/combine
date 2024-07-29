from datetime import datetime
import uuid
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from app import db

class Topic_new(db.Model):
    __tablename__ = 'TCTT_ChuDe'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(255), nullable=False)
    parent_id = db.Column(db.String)
    parent_name = db.Column(db.String)
    status = db.Column(db.String(20), default='Active')
    keyword_platform = db.Column(ARRAY(db.String))
    keyword_spyder = db.Column(ARRAY(db.String))
    created_at = db.Column(db.TIMESTAMP(timezone=True), default=datetime.utcnow)
    added_to_json = db.Column(db.String, default="1")


    @classmethod
    def create(cls, name, created_at, keyword_platform, keyword_spyder, parent_id=None, parent_name=None, status='Active', assign=None, system=None):
        topic = cls(
            name=name,
            parent_id=parent_id,
            parent_name=parent_name,
            status=status,
            system=system,
            keyword_platform=keyword_platform,
            keyword_spyder=keyword_spyder,
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
            'id': str(self.id),
            'name': self.name,
            'parent_id': self.parent_id,
            'parent_name': self.parent_name,
            'status': self.status,
            'system': self.system,
            'keyword_platform': self.keyword_platform,
            'keyword_spyder': self.keyword_spyder,
            'created_at': self.created_at
        }
