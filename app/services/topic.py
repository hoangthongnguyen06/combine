import requests
from datetime import datetime
from app.models import Topic
from app import db

def update_topics_from_api(api_url, headers=None, app=None):
    with app.app_context():
        try:
            payload = {
                "page": 1,
                "size": 1000,
                "data": {
                    "name": "",
                    "organization_id": None,
                    "only_root": True
                },
                "order_field": "created_at",
                "order_type": "DESC"
            }

            response = requests.post(api_url, json=payload, headers=headers, verify=False)
            if response.status_code == 200:
                api_data = response.json().get("data", {}).get("items", [])
                for item in api_data:
                    topic_data = {
                        "id": item["id"],
                        "name": item["name"],
                        "date": datetime.strptime(item["start_at"], "%Y/%m/%d %H:%M:%S"),
                        "parent_id": item.get("topic_parent_id")
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
                    print(f"Updated topic: {topic_data}")
            else:
                print(f"Failed to fetch objects: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"An error occurred with the request: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

