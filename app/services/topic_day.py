from datetime import datetime, timedelta
import requests
from app.models import Post
from app import db
from datetime import datetime
import uuid
from app.models.topic_new import Topic_new
results = db.session.query(Topic_new.uid, Topic_new.name).filter(
    Topic_new.system == 'platform').all()
# page = 66


def update_topic_day_from_api(api_url, headers=None, app=None):
    # Tạo ngày hôm qua và hôm nay
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    yesterday = today - timedelta(days=1)

    # Cập nhật payload với thời gian tương ứng
    payload = {
        "date_from": "2024/01/01 00:00:00",
        "date_to": "2024/07/19 23:59:59",
        "sources": [
            1,
            2,
            4,
            5,
            8,
            9,
            12
        ]
    }
    payload["date_from"] = yesterday.strftime("%Y/%m/%d 00:00:00")
    payload["date_to"] = today.strftime("%Y/%m/%d 23:59:59")

    with app.app_context():
        for topic_id, topic_name in results:
            payload["topic_ids"] = [topic_id]
            try:
                response = requests.post(api_url, json=payload,
                                         headers=headers, verify=False)
                if response.status_code == 200:
                    for details_data in response["data"]:
                        if (details_data["data"]):
                            for details_data_1 in details_data["data"]:
                                extracted_data = {
                                    "uid": str(uuid.uuid4()),
                                    "id_topic": topic_id,
                                    "topic_name": topic_name,
                                    "date": details_data["date"],
                                    "sum_of_posts": details_data_1["total_count"],
                                    "positive_posts": details_data_1["positive_count"],
                                    "neural_posts": details_data_1["neutral_count"],
                                    "negative_posts": details_data_1["negative_count"],
                                    "system": "platform"
                                }
                                # Xu ly nen tang cua tin bai
                                if details_data_1["source_id"] == 1:
                                    extracted_data["platform"] = "Báo chí"
                                elif details_data_1["source_id"] == 2:
                                    extracted_data["platform"] = "Trang điện tử"
                                elif details_data_1["source_id"] == 4:
                                    extracted_data["platform"] = "Blog"
                                elif details_data_1["source_id"] == 5:
                                    extracted_data["platform"] = "Diễn đàn"
                                elif details_data_1["source_id"] == 8:
                                    extracted_data["platform"] = "Facebook"
                                elif details_data_1["source_id"] == 9:
                                    extracted_data["platform"] = "Youtube"
                                elif details_data_1["source_id"] == 12:
                                    extracted_data["platform"] = "Tiktok"
                                top = Post.query.filter_by(
                                    id=extracted_data['id']).first()
                                if top:
                                    for key, value in extracted_data.items():
                                        setattr(top, key, value)
                                    db.session.commit()
                                else:
                                    new_obj = Post(**extracted_data)
                                    db.session.add(new_obj)
                                    db.session.commit()
                else:
                    print(f"Failed to fetch objects: {response.status_code}")
            except requests.exceptions.RequestException as e:
                print(f"An error occurred with the request: {e}")
            except Exception as e:
                print(f"An unexpected error occurred: {e}")

# def create_post(data):
#     post = Post.create(**data)
#     return post


# def update_post(id, data):
#     post = Post.query.get(id)
#     if post:
#         post.update(**data)
#         return post
#     return None


# def delete_post(id):
#     post = Post.query.get(id)
#     if post:
#         post.delete()
#         return True
#     return False


# def get_post(id):
#     return Post.query.get(id)


# def get_all_posts():
#     return Post.query.all()
