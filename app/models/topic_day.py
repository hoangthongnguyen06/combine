from datetime import datetime
from app import db

class Topic_day(db.Model):
    __tablename__ = 'TCTT_ChuDe_Ngay'

    uid = db.Column(db.String, primary_key=True)
    id_topic = db.Column(db.String, db.ForeignKey('TCTT_Chude.uid'), nullable=False)
    topic_name = db.Column(db.String(255), nullable=False)
    sum_of_posts = db.Column(db.Integer, nullable=False)
    positive_posts = db.Column(db.Integer, nullable=False)
    neutral_posts = db.Column(db.Integer, nullable=False)
    negative_posts = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Date, default=datetime.utcnow)
    platform = db.Column(db.String, nullable=False)
    system = db.Column(db.String, nullable=False)
    added_to_json = db.Column(db.String, default="1")

    @classmethod
    def create(cls, uid, id_topic, topic_name, sum_of_posts, positive_post, neutral_post, negative_post, date, platform, system):
        topic_day = cls(
            uid=uid,
            id_topic=id_topic,
            topic_name=topic_name,
            sum_of_posts=sum_of_posts,
            positive_post=positive_post,
            neutral_post=neutral_post,
            negative_post=negative_post,
            date=date,
            platform=platform,
            system=system
        )
        db.session.add(topic_day)
        db.session.commit()
        return topic_day

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
            'id_topic': self.id_topic,
            'topic_name': self.topic_name,
            'sum_of_posts': self.sum_of_posts,
            'positive_post': self.positive_post,
            'neutral_post': self.neutral_post,
            'negative_post': self.negative_post,
            'date': self.date.isoformat(),
            'platform': self.platform,
            'system': self.system
        }
