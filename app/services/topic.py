import requests
from app.models import Topic
from app import db

def update_topics_from_api(api_url, headers=None):
    response = requests.get(api_url, headers=headers)
    if response.status_code == 200:
        topics_data = response.json()
        for topic_data in topics_data:
            topic = Topic.query.filter_by(id=topic_data['id']).first()
            if topic:
                topic.update(**topic_data)
            else:
                Topic.create(**topic_data)
    else:
        print(f"Failed to fetch topics: {response.status_code}")

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
