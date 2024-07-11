from datetime import datetime
from app import db

class Object(db.Model):
    __tablename__ = 'objects'

    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    keys = db.Column(db.String)
    address = db.Column(db.String)
    province = db.Column(db.Integer)
    district = db.Column(db.Integer)
    ward = db.Column(db.Integer)
    longitude = db.Column(db.Float)
    latitude = db.Column(db.Float)
    status = db.Column(db.String(20), default='Active')
    type = db.Column(db.String(50))
    date = db.Column(db.Date, default=datetime.utcnow)

    @classmethod
    def create(cls, name, keys=None, address=None, province=None, district=None, ward=None, longitude=None, latitude=None, type=None):
        obj = cls(
            name=name,
            keys=keys,
            address=address,
            province=province,
            district=district,
            ward=ward,
            longitude=longitude,
            latitude=latitude,
            type=type
        )
        db.session.add(obj)
        db.session.commit()
        return obj

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
            'keys': self.keys,
            'address': self.address,
            'province': self.province,
            'district': self.district,
            'ward': self.ward,
            'longitude': self.longitude,
            'latitude': self.latitude,
            'status': self.status,
            'type': self.type,
            'date': self.date.isoformat()
        }