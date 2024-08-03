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
results_spyder = db.session.query(Topic_new.id, Topic_new.name, Topic_new.keyword_spyder).all()

def update_sentiment_topic_from_api(api_url, headers=None, app=None):
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

    payload_platform["date_from"] = yesterday.strftime("%Y/%m/%d 00:00:00")
    payload_platform["date_to"] = today.strftime("%Y/%m/%d 23:59:59")
    
    now = datetime.now()
    # Tính thời gian 00h của ngày hôm qua
    yesterday_start = datetime(now.year, now.month, now.day) - timedelta(days=1)

    # Tạo payload_spyder với time_range từ 00h ngày hôm qua đến giờ hiện tại
    payload_spyder = {
        "time_range": {
            "from": yesterday_start.strftime("%Y-%m-%d %H:%M:%S"),
            "to": now.strftime("%Y-%m-%d %H:%M:%S")
        },
        "category_id": 16506,
        "top": 10,
        "Topics": [
            -1
        ]
    }

    with app.app_context():
        if Config.PLATFORM_API_URL in api_url:
            for id, name, keyword_platform in results_platform:
                if keyword_platform:
                    # Lặp qua từng từ khóa trong keyword_platform
                    for keyword in keyword_platform:
                        payload_platform["topic_ids"] = [keyword]
                        try:
                            response = requests.post(api_url, json=payload_platform,
                                                    headers=headers, verify=False)
                            if response.status_code == 200:
                                for details_data in response.json().get("data", []):
                                    if details_data.get("data"):
                                        for details_data_1 in details_data["data"]:
                                            extracted_data = {
                                                "uid": str(uuid.uuid4()),
                                                "id_topic": id,
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
        
        elif Config.SPYDER_API_URL in api_url:
            for id, name, keyword_spyder in results_spyder:
                if keyword_spyder:
                    # Lặp qua từng từ khóa trong keyword_spyder
                    for keyword in keyword_spyder:
                        payload_spyder["category_id"] = keyword
                        try:
                            # response = requests.request("POST", api_url, headers=headers, data=payload_spyder)
                            response = requests.post("api_url", json=payload_spyder, headers=headers, verify=False)
                            # print(payload_spyder)
                            # response = requests.post("https://app.spyder.internal/api/category_management/v1/dashboard_topic/overall/sources", json=payload_spyder, headers=headers, verify=False)
                            response.raise_for_status()
                        except requests.exceptions.RequestException as e:
                            print(f"Spyder: An error occurred with the request: {e}")
                            continue  # Skip to the next keyword

                        try:
                            if response.status_code == 200:
                                for details_data in response.json()["result"].get("data", []):
                                    if details_data.get("data"):
                                        total_neutral_posts = sum(item.get("total", 0) for item in details_data["data"])
                                        extracted_data = {
                                            "uid": str(uuid.uuid4()),
                                            "id_topic": id,  
                                            "topic_name": name,
                                            "date": datetime.now().strftime("%Y-%m-%d"),
                                            "sum_of_posts": int(details_data.get("total", 0)),
                                            "positive_posts": None,  # Không có trong JSON trả về, bạn cần thêm logic để xác định giá trị này
                                            "neutral_posts": total_neutral_posts,
                                            "negative_posts": None,  # Không có trong JSON trả về, bạn cần thêm logic để xác định giá trị này
                                            "system": "spyder",
                                            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                            "added_to_json": "0"
                                        }
                                        # Xử lý nền tảng của tin bài
                                        platform_mapping = {
                                            11: "Trang điện tử",
                                            2: "Blog",
                                            3: "Diễn đàn",
                                            1: "Facebook",
                                            4: "Youtube",
                                        }
                                        extracted_data["platform"] = platform_mapping.get(details_data["source_type"], "Unknown")

                                        try:
                                            top = Topic_day.query.filter_by(uid=extracted_data['uid']).first()
                                            if top:
                                                for key, value in extracted_data.items():
                                                    setattr(top, key, value)
                                                db.session.commit()
                                            else:
                                                new_obj = Topic_day(**extracted_data)
                                                db.session.add(new_obj)
                                                db.session.commit()
                                        except Exception as db_e:
                                            print(f"An error occurred while saving to the database: {db_e}")
                            else:
                                print(f"Failed to fetch objects: {response.status_code}")
                        except Exception as e:
                            print(f"An unexpected error occurred: {e}")