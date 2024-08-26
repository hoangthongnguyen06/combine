# app/models/target.py
from app import db
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
import uuid

class Target(db.Model):
    __tablename__ = 'TCTT_DoiTuongCT86'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = db.Column(db.TIMESTAMP(timezone=True), default=datetime.utcnow, nullable=False)
    avatar = db.Column(db.String, nullable=True)
    image = db.Column(db.String, nullable=True)
    name = db.Column(db.String, nullable=True)
    status = db.Column(db.String, nullable=False)
    nuance = db.Column(db.String, nullable=False)
    added_to_json = db.Column(db.String, default="1")
    name_platform = db.Column(db.String, nullable=False)
    id_platform = db.Column(db.UUID(as_uuid=True), default=uuid.uuid4, nullable=False)
    keyword = db.Column(db.String, nullable=False)
    note = db.Column(db.String, nullable=False)
    id_object = db.Column(db.String, nullable=False)
    manage_unit = db.Column(db.UUID(as_uuid=True), default=uuid.uuid4, nullable=False)
    unit = db.Column(db.String, nullable=False)

    def __init__(self, created_at, avatar, image, name, status, nuance, added_to_json, name_platform, id_platform, keyword, note, id_object, manage_unit, unit):
        self.created_at = created_at
        self.avatar = avatar
        self.image = image
        self.name = name
        self.nuance = nuance
        self.status = status
        self.added_to_json = added_to_json
        self.name_platform = name_platform
        self.id_platform = id_platform
        self.keyword = keyword
        self.note = note
        self.id_object = id_object
        self.manage_unit = manage_unit
        self.unit = unit
   