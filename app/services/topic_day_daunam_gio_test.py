from datetime import datetime, timedelta
import requests
import uuid
from app import db
import re
from app.models.topic_new import Topic_new
from app.models.topic_day import Topic_day
from app.config import Config

results_platform = db.session.query(Topic_new.id, Topic_new.name, Topic_new.keyword_platform).all()
results_spyder = db.session.query(Topic_new.id, Topic_new.name, Topic_new.keyword_spyder).all()

def convert_to_number(value):
    if isinstance(value, str):
        value = value.replace(" ", "")
        match = re.match(r"(\d+(\.\d+)?)([KkMm]?)", value)
        if match:
            number = float(match.group(1))
            suffix = match.group(3).lower()

            if suffix == "k":
                number *= 1_000
            elif suffix == "m":
                number *= 1_000_000

            return int(number)
    try:
        return int(value)
    except ValueError:
        return 0

def update_sentiment_topic_from_api(api_url_sac_thai, api_url_tuong_tac, headers=None, app=None):
    now = datetime.now()
    start_date = datetime(2024, 9, 9)  # Ngày bắt đầu là 1/1/2024

    with app.app_context():
        current_date = start_date
        while current_date <= now:
            for hour in range(24):  # Lặp qua từng giờ trong ngày
                date_from = current_date.replace(hour=hour, minute=0, second=0, microsecond=0).strftime("%Y/%m/%d %H:%M:%S")
                date_to = (current_date.replace(hour=hour, minute=59, second=59, microsecond=999999)).strftime("%Y/%m/%d %H:%M:%S")

                payload_platform_sac_thai = {
                    "date_from": date_from,
                    "date_to": date_to,
                    "sources": [1, 2, 4, 5, 8, 9, 12]
                }

                payload_platform_tuong_tac = {
                    "date_from": date_from,
                    "date_to": date_to,
                    "sources": [8, 9, 12]
                }

                payload_spyder_sac_thai = {
                    "time_range": {
                        "from": date_from,
                        "to": date_to
                    },
                    "top": 10,
                    "Topics": [-1]
                }

                # Xử lý platform (platform API)
                if Config.PLATFORM_API_URL in api_url_sac_thai:
                    for id, name, keyword_platform in results_platform:
                        if keyword_platform:
                            for keyword in keyword_platform:
                                payload_platform_sac_thai["topic_ids"] = [keyword]
                                payload_platform_tuong_tac["topic_ids"] = [keyword]
                                try:
                                    response_sacthai = requests.post(api_url_sac_thai, json=payload_platform_sac_thai, headers=headers, verify=False)
                                    response_tuongtac = requests.post(api_url_tuong_tac, json=payload_platform_tuong_tac, headers=headers, verify=False)
                                    response_sacthai.raise_for_status()
                                    response_tuongtac.raise_for_status()
                                except requests.exceptions.RequestException as e:
                                    print(f"An error occurred with the request: {e}")
                                    continue

                                totals = {}
                                try:
                                    if response_sacthai.status_code == 200 and response_tuongtac.status_code == 200:
                                        for details_data in response_tuongtac.json().get("data", []):
                                            for item in details_data.get("list", []):
                                                source_id = item.get("source_id")
                                                if source_id not in totals:
                                                    totals[source_id] = {"share_count": 0, "like_count": 0, "comment_count": 0}
                                                totals[source_id]["share_count"] += item.get("share_count", 0)
                                                totals[source_id]["like_count"] += item.get("like_count", 0)
                                                totals[source_id]["comment_count"] += item.get("comment_count", 0)

                                except Exception as e:
                                    print(f"An error occurred when processing response_tuongtac: {e}")
                                    continue

                                try:
                                    for details_data in response_sacthai.json().get("data", []):
                                        for details_data_1 in details_data["data"]:
                                            try:
                                                source_id = details_data_1.get("source_id")
                                                total_reacts = totals.get(source_id, {}).get("share_count", 0) + totals.get(source_id, {}).get("like_count", 0) + totals.get(source_id, {}).get("comment_count", 0)
                                                extracted_data = {
                                                    "uid": str(uuid.uuid4()),
                                                    "id_topic": id,
                                                    "topic_name": name,
                                                    "date": current_date.strftime("%Y-%m-%d"),
                                                    "hour": hour,
                                                    "sum_of_posts": details_data_1.get("total_count", 0),
                                                    "positive_posts": details_data_1.get("positive_count", 0),
                                                    "neutral_posts": details_data_1.get("neutral_count", 0),
                                                    "negative_posts": details_data_1.get("negative_count", 0),
                                                    "system": "platform",
                                                    "created_at": now.strftime("%Y-%m-%d %H:%M:%S"),
                                                    "added_to_json": "0",
                                                    "reacts": total_reacts,
                                                    "last_updated": now.strftime("%Y-%m-%d %H:%M:%S")
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
                                                    top = Topic_day.query.filter_by(id_topic=extracted_data["id_topic"], system="platform", platform=extracted_data["platform"], date=extracted_data['date'], hour=extracted_data['hour']).first()
                                                    if top:
                                                        extracted_data["added_to_json"] = "2"
                                                        for key, value in extracted_data.items():
                                                            setattr(top, key, value)
                                                        db.session.commit()
                                                    else:
                                                        new_obj = Topic_day(**extracted_data)
                                                        db.session.add(new_obj)
                                                        db.session.commit()
                                                except Exception as db_e:
                                                    print(f"An error occurred while saving to the database: {db_e}")
                                            except Exception as e:
                                                print(f"An error occurred when processing details_data_1: {e}")
                                except Exception as e:
                                    print(f"An error occurred when processing response_sacthai: {e}")

                # Xử lý spyder API
                if Config.SPYDER_API_URL in api_url_sac_thai:
                    for id, name, keyword_spyder in results_spyder:
                        if keyword_spyder:
                            for keyword in keyword_spyder:
                                payload_spyder_sac_thai["category_id"] = keyword
                                try:
                                    response = requests.post(api_url_sac_thai, json=payload_spyder_sac_thai, headers=headers, verify=False)
                                    response.raise_for_status()
                                except requests.exceptions.RequestException as e:
                                    print(f"Spyder: An error occurred with the request: {e}")
                                    continue

                                try:
                                    if response.status_code == 200:
                                        for details_data in response.json()["result"].get("data", []):
                                            total_neutral_posts = sum(convert_to_number(item.get("total", 0)) for item in details_data["data"])
                                            extracted_data = {
                                                "uid": str(uuid.uuid4()),
                                                "id_topic": id,
                                                "topic_name": name,
                                                "date": current_date.strftime("%Y-%m-%d"),
                                                "hour": hour,
                                                "sum_of_posts": int(details_data.get("total", 0)),
                                                "positive_posts": 0,
                                                "neutral_posts": total_neutral_posts,
                                                "negative_posts": 0,
                                                "system": "spyder",
                                                "created_at": now.strftime("%Y-%m-%d %H:%M:%S"),
                                                "added_to_json": "0",
                                                "last_updated": now.strftime("%Y-%m-%d %H:%M:%S")
                                            }

                                            platform_mapping = {
                                                11: "Trang điện tử",
                                                2: "Blog",
                                                3: "Diễn đàn",
                                                1: "Facebook",
                                                4: "Youtube",
                                            }
                                            extracted_data["platform"] = platform_mapping.get(details_data["source_type"], "Unknown")

                                            try:
                                                top = Topic_day.query.filter_by(id_topic=extracted_data["id_topic"], system="spyder", platform=extracted_data["platform"], date=extracted_data['date'], hour=extracted_data['hour']).first()
                                                if top:
                                                    extracted_data["added_to_json"] = "2"
                                                    for key, value in extracted_data.items():
                                                        setattr(top, key, value)
                                                    db.session.commit()
                                                else:
                                                    new_obj = Topic_day(**extracted_data)
                                                    db.session.add(new_obj)
                                                    db.session.commit()
                                            except Exception as db_e:
                                                print(f"Spyder: An error occurred while saving to the database: {db_e}")
                                except Exception as e:
                                    print(f"Spyder: An error occurred when processing response: {e}")

            current_date += timedelta(days=1)  # Tiến đến ngày tiếp theo
