import uuid
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
from app import db

class MucTieuBaoVe_ngay(db.Model):
    __tablename__ = 'TCTT_MucTieuBaoVe_Ngay'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    id_target = db.Column(db.String, db.ForeignKey('TCTT_MucTieuBaoVe.id'), nullable=False)
    target_name = db.Column(db.String(255), nullable=False)
    sum_of_posts = db.Column(db.Integer, nullable=False)
    positive_posts = db.Column(db.Integer, nullable=False, default=0)
    neutral_posts = db.Column(db.Integer, nullable=False)
    negative_posts = db.Column(db.Integer, nullable=False, default=0)
    date = db.Column(db.Date, default=datetime.utcnow)
    platform = db.Column(db.String, nullable=False)
    system = db.Column(db.String, nullable=False)
    created_at = db.Column(db.TIMESTAMP(timezone=True), default=datetime.utcnow)
    added_to_json = db.Column(db.String, default="1")
    reacts = db.Column(db.Integer, nullable=False, default=0)
    last_updated = db.Column(db.TIMESTAMP(timezone=True), default=datetime.utcnow)
    
    @classmethod
    def create(cls, id_target, target_name, sum_of_posts, positive_posts, neutral_posts, negative_posts, date, platform, system, created_at=None, last_updated=None):
        # Set default values for optional fields if not provided
        created_at = created_at or datetime.utcnow()
        last_updated = last_updated or datetime.utcnow()

        # Create a new instance of the model
        new_record = cls(
            id_target=id_target,
            target_name=target_name,
            sum_of_posts=sum_of_posts,
            positive_posts=positive_posts,
            neutral_posts=neutral_posts,
            negative_posts=negative_posts,
            date=date,
            platform=platform,
            system=system,
            created_at=created_at,
            last_updated=last_updated
        )
        
        # Add and commit the new record to the database
        db.session.add(new_record)
        db.session.commit()
        
        return new_record

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
            'uid': str(self.uid),  # Convert UUID to string for serialization
            'id_topic': self.id_topic,
            'topic_name': self.topic_name,
            'sum_of_posts': self.sum_of_posts,
            'positive_posts': self.positive_posts,
            'neutral_posts': self.neutral_posts,
            'negative_posts': self.negative_posts,
            'date': self.date.isoformat(),
            'platform': self.platform,
            'created_at': self.created_at.isoformat(),
            'system': self.system,
            'added_to_json': self.added_to_json
        }


# import uuid
# from datetime import datetime
# from sqlalchemy.dialects.postgresql import UUID
# from app import db

# class MucTieuBaoVe_ngay(db.Model):
#     __tablename__ = 'TCTT_MucTieuBaoVe_Ngay_test'

#     id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
#     id_target = db.Column(db.String, db.ForeignKey('TCTT_MucTieuBaoVe.id'), nullable=False)
#     target_name = db.Column(db.String(255), nullable=False)
#     sum_of_posts = db.Column(db.Integer, nullable=False)
#     positive_posts = db.Column(db.Integer, nullable=False, default=0)
#     neutral_posts = db.Column(db.Integer, nullable=False)
#     negative_posts = db.Column(db.Integer, nullable=False, default=0)
#     date = db.Column(db.Date, default=datetime.utcnow)
#     hour = db.Column(db.Integer, nullable=False, default=lambda: datetime.utcnow().hour)
#     platform = db.Column(db.String, nullable=False)
#     system = db.Column(db.String, nullable=False)
#     created_at = db.Column(db.TIMESTAMP(timezone=True), default=datetime.utcnow)
#     added_to_json = db.Column(db.String, default="1")
#     reacts = db.Column(db.Integer, nullable=False, default=0)
#     last_updated = db.Column(db.TIMESTAMP(timezone=True), default=datetime.utcnow)
    
#     @classmethod
#     def create(cls, id_target, target_name, sum_of_posts, positive_posts, neutral_posts, negative_posts, date, hour, platform, system, created_at=None, last_updated=None):
#         # Set default values for optional fields if not provided
#         created_at = created_at or datetime.utcnow()
#         last_updated = last_updated or datetime.utcnow()

#         # Create a new instance of the model
#         new_record = cls(
#             id_target=id_target,
#             target_name=target_name,
#             sum_of_posts=sum_of_posts,
#             positive_posts=positive_posts,
#             neutral_posts=neutral_posts,
#             negative_posts=negative_posts,
#             date=date,
#             platform=platform,
#             system=system,
#             created_at=created_at,
#             last_updated=last_updated,
#             hour=hour
#         )
        
#         # Add and commit the new record to the database
#         db.session.add(new_record)
#         db.session.commit()
        
#         return new_record

#     def update(self, **kwargs):
#         for key, value in kwargs.items():
#             setattr(self, key, value)
#         db.session.commit()

#     def delete(self):
#         db.session.delete(self)
#         db.session.commit()

#     @classmethod
#     def get_all(cls):
#         return cls.query.all()

#     @classmethod
#     def get_by_id(cls, uid):
#         return cls.query.get(uid)

#     def serialize(self):
#         return {
#             'uid': str(self.uid),  # Convert UUID to string for serialization
#             'id_topic': self.id_topic,
#             'topic_name': self.topic_name,
#             'sum_of_posts': self.sum_of_posts,
#             'positive_posts': self.positive_posts,
#             'neutral_posts': self.neutral_posts,
#             'negative_posts': self.negative_posts,
#             'date': self.date.isoformat(),
#             'hour': self.hour,
#             'platform': self.platform,
#             'created_at': self.created_at.isoformat(),
#             'system': self.system,
#             'added_to_json': self.added_to_json
#         }
