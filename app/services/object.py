import requests
from app.models import Object
from app import db

def update_objects_from_api(api_url, headers=None):
    response = requests.get(api_url, headers=headers)
    if response.status_code == 200:
        objects_data = response.json()
        for object_data in objects_data:
            obj = Object.query.filter_by(id=object_data['id']).first()
            if obj:
                obj.update(**object_data)
            else:
                Object.create(**object_data)
    else:
        print(f"Failed to fetch objects: {response.status_code}")

def create_object(data):
    obj = Object.create(**data)
    return obj

def update_object(id, data):
    obj = Object.query.get(id)
    if obj:
        obj.update(**data)
        return obj
    return None

def delete_object(id):
    obj = Object.query.get(id)
    if obj:
        obj.delete()
        return True
    return False

def get_object(id):
    return Object.query.get(id)

def get_all_objects():
    return Object.query.all()
