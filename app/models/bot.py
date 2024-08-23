from app import db
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID, ARRAY
import uuid
class BotCT86(db.Model):
    __tablename__ = 'TCTT_BotCT86'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    uid = db.Column(db.String(20))
    email = status = db.Column(db.String, default=None)
    unit_id =  db.Column(db.UUID(as_uuid=True), default=uuid.uuid4, nullable=False)
    created_at = db.Column(db.TIMESTAMP(timezone=True), default=datetime.utcnow, nullable=True)
    updated_at = db.Column(db.TIMESTAMP(timezone=True), default=datetime.utcnow, nullable=True)
    status = db.Column(db.String(20), default='Active')

    def __init__(self, uid, created_at, updated_at, status, unit_id, email):
        self.email = email
        self.uid = uid
        self.created_at = created_at
        self.status = status
        self.updated_at = updated_at
        self.unit_id = unit_id