import requests
from datetime import datetime
from app import db
from app.models import Topic
from flask import current_app
import requests
from datetime import datetime
import requests
from flask import current_app
from app import db
from app.models import Topic

def update_topics_from_api(api_url, headers=None):
    payload = {
        "page": 1,
        "size": 1000,
        "data": {
            "name": "",
            "organization_id": "null",
            "only_root": "true"
        },
        "order_field": "created_at",
        "order_type": "DESC"
    }

    try:
        with current_app.app_context():
            response = requests.post(api_url, json=payload, headers=headers, verify=False)
            if response.status_code == 200:
                api_data = response.json().get("data", {}).get("items", [])
                for item in api_data:
                    topic_data = {
                        "id": item["id"],
                        "name": item["name"],
                        "date": item["start_at"],
                        "parent_id": item["topic_parent_id"]
                    }
                    end_at = item.get("end_at")
                    if end_at:
                        end_at_datetime = datetime.strptime(end_at, "%Y/%m/%d %H:%M:%S")
                        if end_at_datetime < datetime.now():
                            topic_data["status"] = "deactive"
                        else:
                            topic_data["status"] = "active"
                    
                    topic = Topic.query.filter_by(id=topic_data['id']).first()
                    if topic:
                        for key, value in topic_data.items():
                            setattr(topic, key, value)
                    else:
                        topic = Topic(**topic_data)
                        db.session.add(topic)
                    
                    db.session.commit()
            else:
                print(f"Failed to fetch objects: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred with the request: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def create_topic(data):
    topic = Topic.create(**data)
    return topic

def update_topic(id, data):
    topic = Topic.query.get(id)
    if topic:
        topic.update(**data)
        return topic
    return None

def delete_topic(id):
    topic = Topic.query.get(id)
    if topic:
        topic.delete()
        return True
    return False

def get_topic(id):
    return Topic.query.get(id)

def get_all_topics():
    return Topic.query.all()
