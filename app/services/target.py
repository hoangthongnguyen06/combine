import requests
from app.models import Target
from app import db

def update_targets_from_api(api_url, headers=None):
    response = requests.get(api_url, headers=headers)
    if response.status_code == 200:
        targets_data = response.json()
        for target_data in targets_data:
            target = Target.query.filter_by(id=target_data['id']).first()
            if target:
                target.update(**target_data)
            else:
                Target.create(**target_data)
    else:
        print(f"Failed to fetch targets: {response.status_code}")

def create_target(data):
    target = Target.create(**data)
    return target

def update_target(id, data):
    target = Target.query.get(id)
    if target:
        target.update(**data)
        return target
    return None

def delete_target(id):
    target = Target.query.get(id)
    if target:
        target.delete()
        return True
    return False

def get_target(id):
    return Target.query.get(id)

def get_all_targets():
    return Target.query.all()
