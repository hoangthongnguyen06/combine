from datetime import datetime
from app import db

class Result(db.Model):
    __tablename__ = 'TCTT_Result'

    id = db.Column(db.String, primary_key=True)
    account_id = db.Column(db.String, db.ForeignKey('targets.id'))
    post_id = db.Column(db.String, db.ForeignKey('posts.id'))
    bots_number = db.Column(db.Integer)
    completed_time = db.Column(db.Time)
    status = db.Column(db.String(20), default='Processing')
    type = db.Column(db.String(20), default='ProActive')

    @classmethod
    def create(cls, account_id, post_id, bots_number=None, completed_time=None, status=None, type=None):
        result = cls(
            account_id=account_id,
            post_id=post_id,
            bots_number=bots_number,
            completed_time=completed_time,
            status=status,
            type=type
        )
        db.session.add(result)
        db.session.commit()
        return result

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
            'account_id': self.account_id,
            'post_id': self.post_id,
            'bots_number': self.bots_number,
            'completed_time': self.completed_time.isoformat() if self.completed_time else None,
            'status': self.status,
            'type': self.type
        }