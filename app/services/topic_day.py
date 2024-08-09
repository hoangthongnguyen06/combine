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

def update_sentiment_topic_from_api(api_url_sac_thai, api_url_tuong_tac, headers=None, app=None):
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    yesterday = today - timedelta(days=1)

    payload_platform_sac_thai = {
        "date_from": today.strftime("%Y/%m/%d 00:00:00"),
        "date_to": today.strftime("%Y/%m/%d 23:59:59"),
        "sources": [1, 2, 4, 5, 8, 9, 12]
    }

    payload_platform_tuong_tac = {
        "date_from": today.strftime("%Y/%m/%d 00:00:00"),
        "date_to": today.strftime("%Y/%m/%d 23:59:59"),
        "sources": [8, 9, 12]
    }

    now = datetime.now()
    yesterday_start = datetime(now.year, now.month, now.day) - timedelta(days=1)
    
    payload_spyder_sac_thai = {
        "time_range": {
            "from": yesterday_start.strftime("%Y-%m-%d %H:%M:%S"),
            "to": now.strftime("%Y-%m-%d %H:%M:%S")
        },
        "top": 10,
        "Topics": [-1]
    }

#     payload_spyder_sac_thai = {
#     "time_range": {
#         "from": "2024-01-01 23:59:59",
#         "to": "2024-08-09 23:59:59"
#     },
#     "top": 10,
#     "Topics": [-1]
# }

    with app.app_context():
        if Config.PLATFORM_API_URL in api_url_sac_thai:
            for id, name, keyword_platform in results_platform:
                if keyword_platform:
                    for keyword in keyword_platform:
                        payload_platform_sac_thai["topic_ids"] = [keyword]
                        payload_platform_tuong_tac["topic_ids"] = [keyword]
                        try:
                            response_sacthai = requests.post(api_url_sac_thai, json=payload_platform_sac_thai, headers=headers, verify=False)
                            response_tuongtac = requests.post(api_url_tuong_tac, json=payload_platform_tuong_tac, headers=headers, verify=False)
                            print(response_tuongtac.json())
                            response_sacthai.raise_for_status()
                            response_tuongtac.raise_for_status()
                        except requests.exceptions.RequestException as e:
                            print(f"An error occurred with the request: {e}")
                            continue
                        totals = {}       
                        try:
                            if response_sacthai.status_code == 200 and response_tuongtac.status_code == 200:
                                
                                for details_data in response_tuongtac.json().get("data", []):
                                    print(details_data)
                                    for item in details_data.get("list", []):
                                        # print("item", item)
                                        source_id = item.get("source_id")
                                        if source_id not in totals:
                                            totals[source_id] = {"share_count": 0, "like_count": 0, "comment_count": 0}
                                        totals[source_id]["share_count"] += item.get("share_count", 0)
                                        totals[source_id]["like_count"] += item.get("like_count", 0)
                                        totals[source_id]["comment_count"] += item.get("comment_count", 0)
                                # print("Total", totals)
                        except KeyError as e:
                            print(f"Key error when processing response_tuongtac: {e}")
                            continue
                        except AttributeError as e:
                            print(f"Attribute error when processing response_tuongtac: {e}")
                            continue
                        except Exception as e:
                            print(f"An unexpected error occurred when processing response_tuongtac: {e}")
                            continue

                        try:
                            for details_data in response_sacthai.json().get("data", []):
                                if details_data.get("data"):
                                    for details_data_1 in details_data["data"]:
                                        try:
                                            source_id = details_data_1.get("source_id")
                                            total_reacts = totals.get(source_id, {}).get("share_count", 0) + totals.get(source_id, {}).get("like_count", 0) + totals.get(source_id, {}).get("comment_count", 0)
                                            extracted_data = {
                                                "uid": str(uuid.uuid4()),
                                                "id_topic": id,
                                                "topic_name": name,
                                                "date": details_data.get("date"),
                                                "sum_of_posts": details_data_1.get("total_count", 0),
                                                "positive_posts": details_data_1.get("positive_count", 0),
                                                "neutral_posts": details_data_1.get("neutral_count", 0),
                                                "negative_posts": details_data_1.get("negative_count", 0),
                                                "system": "platform",
                                                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                                "added_to_json": "0",
                                                "reacts": total_reacts,
                                                "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                            }

                                            platform_mapping = {
                                                1: "Báo chí",
                                                2: "Trang điện tử",
                                                4: "Blog",
                                                5: "Diễn đàn",
                                                8: "Facebook",
                                                9: "Youtube",
                                                12: "Tiktok"
                                            }
                                            extracted_data["platform"] = platform_mapping.get(source_id, "Unknown")
                                            try:
                                                top = Topic_day.query.filter_by(id_topic=extracted_data["id_topic"], platform=extracted_data["platform"], date=extracted_data['date']).first()
                                                if top:
                                                    extracted_data["added_to_json"] = "2"  # Updated value
                                                    for key, value in extracted_data.items():
                                                        setattr(top, key, value)
                                                    db.session.commit()
                                                else:
                                                    new_obj = Topic_day(**extracted_data)
                                                    db.session.add(new_obj)
                                                    db.session.commit()
                                            except Exception as db_e:
                                                print(f"An error occurred while saving to the database: {db_e}")
                                        except KeyError as e:
                                            print(f"Key error when processing details_data_1: {e}")
                                        except AttributeError as e:
                                            print(f"Attribute error when processing details_data_1: {e}")
                                        except Exception as e:
                                            print(f"An unexpected error occurred when processing details_data_1: {e}")
                        except KeyError as e:
                            print(f"Key error when processing response_sacthai: {e}")
                        except AttributeError as e:
                            print(f"Attribute error when processing response_sacthai: {e}")
                        except Exception as e:
                            print(f"An unexpected error occurred when processing response_sacthai: {e}")
        
        
        elif Config.SPYDER_API_URL in api_url_sac_thai:
            for id, name, keyword_spyder in results_spyder:
                if keyword_spyder:
                    # Lặp qua từng từ khóa trong keyword_spyder
                    for keyword in keyword_spyder:
                        payload_spyder_sac_thai["category_id"] = keyword
                        try:
                            # response = requests.request("POST", api_url, headers=headers, data=payload_spyder)
                            response = requests.post(api_url_sac_thai, json=payload_spyder_sac_thai, headers=headers, verify=False)
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
                                            "positive_posts": 0,  # Không có trong JSON trả về, bạn cần thêm logic để xác định giá trị này
                                            "neutral_posts": total_neutral_posts,
                                            "negative_posts": 0,  # Không có trong JSON trả về, bạn cần thêm logic để xác định giá trị này
                                            "system": "spyder",
                                            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                            "added_to_json": "0", 
                                            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
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
                                            top = Topic_day.query.filter_by(id_topic=extracted_data["id_topic"],system="spyder", platform=extracted_data["platform"], date=extracted_data['date']).first()
                                            if top:
                                                extracted_data["added_to_json"] = "2"  # Updated value
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