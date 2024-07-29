from datetime import datetime, timedelta
import requests
from app import db
from datetime import datetime
import uuid
from app.models.topic_new import Topic_new
from app.config import Config
from uuid import UUID
from app.models.topic_day import Topic_day
results_platform = db.session.query(Topic_new.id, Topic_new.name, Topic_new.keyword_platform).all()
# page = 66
# results_spyder = db.session.query(Topic_new.uid, Topic_new.name).filter(
#     Topic_new.system == 'spyder').all()


def update_sentiment_topic_from_api(api_url, headers_platform=None, app=None):
    # Tạo ngày hôm qua và hôm nay
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    yesterday = today - timedelta(days=1)

    # Cập nhật payload với thời gian tương ứng
    payload_platform = {
        "date_from": "2024/01/01 00:00:00",
        "date_to": "2024/07/29 23:59:59",
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

    # payload_platform["date_from"] = yesterday.strftime("%Y/%m/%d 00:00:00")
    # payload_platform["date_to"] = today.strftime("%Y/%m/%d 23:59:59")

    payload_spyder = {
        "time_range": {
            "from": "2024-01-01 00:00:00",
            "to": "2024-01-01 23:59:59"
        },
        "category_id": 16064,
        "top": 5,
        "Topics": [
            -1
        ]
    }

    start_date = datetime.strptime("2024-01-01", "%Y-%m-%d")
    end_date = datetime.strptime("2024-07-19", "%Y-%m-%d")

    current_date = start_date


    with app.app_context():
        if Config.PLATFORM_API_URL in api_url:
            for id, name, keyword_platform in results_platform:
                # Lặp qua từng từ khóa trong keyword_platform
                for keyword in keyword_platform:
                    payload_platform["topic_ids"] = [keyword]
                    try:
                        response = requests.post(api_url, json=payload_platform,
                                                 headers=headers_platform, verify=False)
                        if response.status_code == 200:
                            for details_data in response.json().get("data", []):
                                if details_data.get("data"):
                                    for details_data_1 in details_data["data"]:
                                        extracted_data = {
                                            "uid": str(uuid.uuid4()),
                                            "id_topic": UUID(id),
                                            "topic_name": name,
                                            "date": details_data["date"],
                                            "sum_of_posts": details_data_1["total_count"],
                                            "positive_posts": details_data_1["positive_count"],
                                            "neutral_posts": details_data_1["neutral_count"],
                                            "negative_posts": details_data_1["negative_count"],
                                            "system": "platform",
                                            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                            "added_to_json": "0"
                                        }
                                        # Xử lý nền tảng của tin bài
                                        platform_mapping = {
                                            1: "Báo chí",
                                            2: "Trang điện tử",
                                            4: "Blog",
                                            5: "Diễn đàn",
                                            8: "Facebook",
                                            9: "Youtube",
                                            12: "Tiktok"
                                        }
                                        extracted_data["platform"] = platform_mapping.get(details_data_1["source_id"], "Unknown")

                                        top = Topic_day.query.filter_by(uid=extracted_data['uid']).first()
                                        if top:
                                            for key, value in extracted_data.items():
                                                setattr(top, key, value)
                                            db.session.commit()
                                        else:
                                            new_obj = Topic_day(**extracted_data)
                                            db.session.add(new_obj)
                                            db.session.commit()
                        else:
                            print(f"Failed to fetch objects: {response.status_code}")
                    except requests.exceptions.RequestException as e:
                        print(f"An error occurred with the request: {e}")
                    except Exception as e:
                        print(f"An unexpected error occurred: {e}")
        # elif Config.SPYDER_API_URL in api_url:
        #     for topic_id, topic_name in results_spyder:
        #         payload_spyder["category_id"] = topic_id
        #         while current_date <= end_date:
        #             date_str = current_date.strftime("%Y-%m-%d")
        #             payload_spyder["time_range"]["from"] = f"{date_str} 00:00:00"
        #             payload_spyder["time_range"]["to"] = f"{date_str} 23:59:59"

        #             current_date += timedelta(days=1)
        #             try:
        #                 api_data = requests.post(api_url, json=payload_spyder,
        #                                          headers=headers, verify=False)
        #                 if api_data.status_code == 200:
        #                     result_data = api_data["result"]
        #                     extracted_data = {
        #                         "uid": str(uuid.uuid4()),
        #                         "id_topic": topic_id,
        #                         "topic_name": topic_name,
        #                         "date": current_date,
        #                         "sum_of_posts": result_data["total_post"],
        #                         "positive_posts": result_data["total_positive"],
        #                         "neural_posts": result_data["total_neutral"],
        #                         "negative_posts": result_data["total_negative"],
        #                         "system": "spyder"
        #                     }
        #                 else:
        #                     print(
        #                         f"Failed to fetch objects: {response.status_code}")
        #             except requests.exceptions.RequestException as e:
        #                 print(f"An error occurred with the request: {e}")
        #             except Exception as e:
        #                 print(f"An unexpected error occurred: {e}")

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
