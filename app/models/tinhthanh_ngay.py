from app import db
from datetime import datetime
import uuid  # Import uuid để sử dụng trong việc tạo UUID

class Tinhthanh_Ngay(db.Model):
    __tablename__ = 'TCTT_Tinhthanh_Ngay'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # Thêm trường id với kiểu Integer, tự động tăng
    id_province = db.Column(db.UUID(as_uuid=True), default=uuid.uuid4, nullable=False)  # Sử dụng UUID
    name_province = db.Column(db.String(100), nullable=False)
    sum_of_posts = db.Column(db.Integer, nullable=False, default=0)
    positive_posts = db.Column(db.Integer, nullable=False, default=0)
    neutral_posts = db.Column(db.Integer, nullable=False, default=0)
    negative_posts = db.Column(db.Integer, nullable=False, default=0)
    added_to_json = db.Column(db.String, default="1")
    date = db.Column(db.Date, default=datetime.utcnow)
    last_updated = db.Column(db.TIMESTAMP(timezone=True), default=datetime.utcnow, nullable=False)
    created_at = db.Column(db.TIMESTAMP(timezone=True), default=datetime.utcnow, nullable=False)
    reacts = db.Column(db.Integer, nullable=False, default=0)

    def __init__(self, id_province, name_province, sum_of_posts=0, positive_posts=0, neutral_posts=0, 
                 negative_posts=0, reacts=0, added_to_json="1", date=None, last_updated=None, created_at=None):
        self.id_province = id_province
        self.name_province = name_province
        self.sum_of_posts = sum_of_posts
        self.positive_posts = positive_posts
        self.neutral_posts = neutral_posts
        self.negative_posts = negative_posts
        self.reacts = reacts
        self.added_to_json = added_to_json
        self.date = date if date else datetime.utcnow()
        self.last_updated = last_updated if last_updated else datetime.utcnow()
        self.created_at = created_at if created_at else datetime.utcnow()
    

    def __repr__(self):
        return f'<Statistics {self.name_province}>'
