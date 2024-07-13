import requests
from app.models import Topic
from datetime import datetime
from app import db

def update_topics_from_api(api_url, headers=None):
    print(api_url)
    response = requests.get(api_url, headers=headers)
    if response.status_code == 200:
        api_data = response.json()
        items = api_data.post("data", {}).get("items", [])

        for item in items:
            topic_data = {
                "id": item["id"],
                "name": item["name"],
                "date": item["start_at"],
                "parent_id": item["topic_parent_id"]
                # Add other fields you need here
            }
            # Check if end_at is expired
            end_at = item.get("end_at")
            if end_at:
                end_at_datetime = datetime.strptime(end_at, "%Y/%m/%d %H:%M:%S")
                if end_at_datetime < datetime.now():
                    topic_data["status"] = "deactive"
                else:
                    topic_data["status"] = "active"
            top = Topic.query.filter_by(id=topic_data['id']).first()
            if top:
                for key, value in topic_data.items():
                    setattr(top, key, value)
                db.session.commit()
            else:
                new_obj = Topic(**topic_data)
                db.session.add(new_obj)
                db.session.commit()
            print(item)
    else:
        print(f"Failed to fetch objects: {response.status_code}")

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
