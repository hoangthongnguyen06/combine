import requests
from app.models import Tinhthanh_Ngay
from app import db
import app
from datetime import datetime, timedelta
from app.config import Config
from app import endpoints
import uuid
def get_province_data(api_url, headers=None):
    try:
        response = requests.get(api_url, headers=headers, verify=False)
        response.raise_for_status()
        
        api_data = response.json()
        province_list = api_data.get("data", [])
        
        # Tạo một từ điển để ánh xạ name_province và id_province
        province_code_map = {
            province["name"]: province["id"]
            for province in province_list
        }
        
        return province_code_map
    
    except requests.RequestException as e:
        print(f"API request failed: {e}")
        return {}
    
    except ValueError as e:
        print(f"Error parsing JSON response: {e}")
        return {}

def update_location_post_counts_from_api(api_url, headers=None, province_api_url=None, app=None):
    # Lấy dữ liệu tỉnh thành và id_province từ API khác
    province_code_map = get_province_data(endpoints.APISupabase.TINHTHANH_NGAY.value, headers)
    
    if not province_code_map:
        print("Failed to retrieve province data.")
        return
    
    with app.app_context():
        # Tạo payload với thời gian từ 7 ngày trước đến thời điểm hiện tại
        date_to = datetime.now()
        date_from = date_to - timedelta(days=7)
        
        payload = {
            "date_from": date_from.strftime("%Y/%m/%d %H:%M:%S"),
            "date_to": date_to.strftime("%Y/%m/%d %H:%M:%S"),
            "topic_ids": None,
            "sentiment": None
        }

        try:
            response = requests.post(api_url, json=payload, headers=headers, verify=False)
            response.raise_for_status()  # Kiểm tra xem yêu cầu có thành công hay không

            api_data = response.json()
            locations = api_data.get("data", {}).get("locations", [])

            for loc in locations:
                location_name = loc.get("location")
                location_id_str = province_code_map.get(location_name)
                # Chuyển đổi location_id_str thành UUID nếu cần thiết
                try:
                    location_id = uuid.UUID(location_id_str)
                except ValueError:
                    print(f"Invalid UUID format for location ID: {location_id_str}")
                    continue

                if location_id:
                    location_data = {
                        "id_province": location_id,
                        "name_province": location_name,
                        "sum_of_posts": loc.get("total_count", 0),
                        "positive_posts": loc.get("positive_count", 0),
                        "neutral_posts": loc.get("neutral_count", 0),
                        "negative_posts": loc.get("negative_count", 0),
                        "reacts": loc.get("reacts", 0),  # Kiểm tra có trường reacts không, nếu không có thì loại bỏ
                        "date": date_to.strftime("%Y-%m-%d"),
                        "last_updated": datetime.now(),
                        "created_at": datetime.now(),
                        "added_to_json": "1"  # Giá trị mặc định cho bản ghi mới
                    }

                    try:
                        existing_location = Tinhthanh_Ngay.query.filter_by(id_province=location_data["id_province"], date=location_data["date"]).first()
                        if existing_location:
                            # Cập nhật thông tin nếu bản ghi đã tồn tại
                            existing_location.sum_of_posts = location_data["sum_of_posts"]
                            existing_location.positive_posts = location_data["positive_posts"]
                            existing_location.neutral_posts = location_data["neutral_posts"]
                            existing_location.negative_posts = location_data["negative_posts"]
                            existing_location.reacts = location_data["reacts"]
                            existing_location.last_updated = location_data["last_updated"]
                            existing_location.added_to_json = "2"
                        else:
                            # Tạo bản ghi mới nếu chưa tồn tại
                            new_location = Tinhthanh_Ngay(**location_data)
                            db.session.add(new_location)

                        db.session.commit()

                    except Exception as e:
                        db.session.rollback()
                        print(f"Error updating database: {e}")

        except requests.RequestException as e:
            print(f"API request failed: {e}")

        except ValueError as e:
            print(f"Error parsing JSON response: {e}")