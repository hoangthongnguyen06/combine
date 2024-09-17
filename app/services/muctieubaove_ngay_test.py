import re

def convert_to_number(value):
    if isinstance(value, str):
        # Loại bỏ khoảng trắng
        value = value.replace(" ", "")
        # Dùng regex để lấy phần số và hậu tố (K, M)
        match = re.match(r"(\d+(\.\d+)?)([KkMm]?)", value)
        if match:
            number = float(match.group(1))  # Phần số
            suffix = match.group(3).lower()  # Hậu tố

            if suffix == "k":
                number *= 1_000
            elif suffix == "m":
                number *= 1_000_000

            return int(number)  # Trả về số nguyên
    try:
        return int(value)  # Trường hợp không có hậu tố, trả về số nguyên
    except ValueError:
        return 0  # Trường hợp giá trị không phải số, trả về 0



from datetime import datetime, timedelta
import requests
from app import db
from datetime import datetime
import uuid
from app.models.muctieubaove import MucTieuBaoVe
from app.models.muctieubaove_ngay import MucTieuBaoVe_ngay
from app.config import Config
from uuid import UUID
results_platform = db.session.query(MucTieuBaoVe.id, MucTieuBaoVe.name, MucTieuBaoVe.keyword_platform).all()
results_spyder = db.session.query(MucTieuBaoVe.id, MucTieuBaoVe.name, MucTieuBaoVe.keyword_spyder).all()
def update_sentiment_target_from_api(api_url_sac_thai, api_url_tuong_tac, headers=None, app=None):
    now = datetime.now()
    one_hour_ago = now - timedelta(hours=1)
    
    payload_platform_sac_thai = {
        "date_from": one_hour_ago.strftime("%Y/%m/%d %H:00:00"),
        "date_to": now.strftime("%Y/%m/%d %H:00:00"),
        "sources": [1, 2, 4, 5, 8, 9, 12]
    }

    payload_platform_tuong_tac = {
        "date_from": one_hour_ago.strftime("%Y/%m/%d %H:00:00"),
        "date_to": now.strftime("%Y/%m/%d %H:00:00"),
        "sources": [8, 9, 12]
    }

    payload_spyder_sac_thai = {
        "time_range": {
            "from": one_hour_ago.strftime("%Y-%m-%d %H:%M:%S"),
            "to": now.strftime("%Y-%m-%d %H:%M:%S")
        },
        "top": 10,
        "Topics": [-1]
    }

    
    with app.app_context():
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
                                            "id_target": id,
                                            "target_name": name,
                                            "date": details_data.get("date"),
                                            "hour": one_hour_ago.hour,
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
                                            top = MucTieuBaoVe_ngay.query.filter_by(id_target=extracted_data["id_target"], system="platform", platform=extracted_data["platform"], date=extracted_data['date'], hour=extracted_data['hour']).first()
                                            if top:
                                                extracted_data["added_to_json"] = "2"
                                                for key, value in extracted_data.items():
                                                    setattr(top, key, value)
                                                db.session.commit()
                                            else:
                                                new_obj = MucTieuBaoVe_ngay(**extracted_data)
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
                                        "id_target": id,
                                        "target_name": name,
                                        "date": now.strftime("%Y-%m-%d"),
                                        "hour": one_hour_ago.hour,
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
                                        top = MucTieuBaoVe_ngay.query.filter_by(id_target=extracted_data["id_target"], system="spyder", platform=extracted_data["platform"], date=extracted_data['date'], hour=extracted_data['hour']).first()
                                        if top:
                                            extracted_data["added_to_json"] = "2"
                                            for key, value in extracted_data.items():
                                                setattr(top, key, value)
                                            db.session.commit()
                                        else:
                                            new_obj = MucTieuBaoVe_ngay(**extracted_data)
                                            db.session.add(new_obj)
                                            db.session.commit()
                                    except Exception as db_e:
                                        print(f"An error occurred while saving to the database: {db_e}")
                            else:
                                print(f"Failed to fetch objects: {response.status_code}")
                        except Exception as e:
                            print(f"An error occurred when processing response: {e}")
