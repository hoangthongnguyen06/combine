import requests
from app.models import Result
from app import db

def update_results_from_api(api_url, headers=None):
    response = requests.get(api_url, headers=headers)
    if response.status_code == 200:
        results_data = response.json()
        for result_data in results_data:
            result = Result.query.filter_by(id=result_data['id']).first()
            if result:
                result.update(**result_data)
            else:
                Result.create(**result_data)
    else:
        print(f"Failed to fetch results: {response.status_code}")

def create_result(data):
    result = Result.create(**data)
    return result

def update_result(id, data):
    result = Result.query.get(id)
    if result:
        result.update(**data)
        return result
    return None

def delete_result(id):
    result = Result.query.get(id)
    if result:
        result.delete()
        return True
    return False

def get_result(id):
    return Result.query.get(id)

def get_all_results():
    return Result.query.all()
