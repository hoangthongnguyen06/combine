from app import db
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID, ARRAY
import uuid

class ServerCT(db.Model):
    __tablename__ = 'server_ct86'
    __table_args__ = {'schema': 'btth'}
    uuid = db.Column(UUID(as_uuid=True), primary_key=True)
    cpu = db.Column(db.String(20), default=None)
    unit_id_manager = db.Column(db.String(100), nullable=True)
    last_up = db.Column(db.TIMESTAMP(timezone=True), default=datetime.utcnow, nullable=False)
    ip = db.Column(ARRAY(db.String), nullable=False)
    status = db.Column(db.String(20), default='up')
    storage = db.Column(db.Integer, nullable=True)
    ram = db.Column(db.Integer, nullable=False, default=0)
    host_name = db.Column(db.String(100), nullable=True)

    def __init__(self, uuid, cpu, unit_id_manager, last_up,  ip, status,
                 storage, ram, host_name):
        self.uuid = uuid
        self.cpu = cpu
        self.unit_id_manager = unit_id_manager
        self.last_up = last_up if last_up else datetime.utcnow()
        self.ip = ip
        self.status = status
        self.storage = storage
        self.ram = ram
        self.host_name = host_name
