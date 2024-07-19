import requests
from datetime import datetime
from uuid import UUID
from app.models import Topic_new
from app import db

payload_platform = {
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

def update_topics_new_from_api(api_url, headers_platform=None,headers_spyder=None, app=None):
    with app.app_context():
        if "platform" in api_url:
            try:
                response = requests.post(api_url, json=payload_platform, headers=headers_platform, verify=False)
                if response.status_code == 200:
                    api_data = response.json().get("data", {}).get("items", [])
                    for item in api_data:
                        topic_data = {
                            "uid": str(item["id"]),  # Chuyển đổi thành chuỗi
                            "name": item["name"],
                            "parent_id": item.get("topic_parent_id"),
                            "assign": item.get("org_name"),
                            "system": "platform"
                        }
                        end_at = item.get("end_at")
                        if end_at:
                            end_at_datetime = datetime.strptime(end_at, "%Y/%m/%d %H:%M:%S")
                            if end_at_datetime < datetime.now():
                                topic_data["status"] = "deactive"
                            else:
                                topic_data["status"] = "active"
                        topic = Topic_new.query.filter_by(id=topic_data['id']).first()
                        if topic:
                            for key, value in topic_data.items():
                                setattr(topic, key, value)
                        else:
                            topic = Topic_new(**topic_data)
                            db.session.add(topic)
                        
                        db.session.commit()
                        print(f"Updated topic: {topic_data}")
                else:
                    print(f"PLATFORM: Failed to fetch objects: {response.status_code}")
            except requests.exceptions.RequestException as e:
                print(f"PLATFORM: An error occurred with the request: {e}")
            except Exception as e:
                print(f"PLATFORM: An unexpected error occurred: {e}")
        if "spider" in api_url:
            print("spider")
            try:
                response = requests.post(api_url, json=payload_platform, headers=headers_spyder, verify=False)
                if response.status_code == 200:
                    api_data = response.json().get("result", {}).get("data", [])
                    for item in api_data:
                        topic_data = {
                            "uid": str(item["id"]),  # Chuyển đổi thành chuỗi
                            "name": item["name"],
                            "assign": item.get("create_by"),
                            "system": "spyder"
                        }
                        if item.get("topic_parent_id"):
                            topic_data["parent_id"] =  item.get("topic_parent_id"),
                        else: topic_data["parent_id"] == ""
                        end_at = item.get("expired_date")
                        if end_at:
                            end_at_datetime = datetime.strptime(end_at, "%Y/%m/%d %H:%M:%S")
                            if end_at_datetime < datetime.now():
                                topic_data["status"] = "deactive"
                            else:
                                topic_data["status"] = "active"
                        topic = Topic_new.query.filter_by(id=topic_data['id']).first()
                        if topic:
                            for key, value in topic_data.items():
                                setattr(topic, key, value)
                        else:
                            topic = Topic_new(**topic_data)
                            db.session.add(topic)
                        
                        db.session.commit()
                        print(f"Updated topic: {topic_data}")
                else:
                    print(f"SPYDER: Failed to fetch objects: {response.status_code}")
            except requests.exceptions.RequestException as e:
                print(f"SPYDER: An error occurred with the request: {e}")
            except Exception as e:
                print(f"SPYDER: An unexpected error occurred: {e}")
        else:
            print("get data from ct86")