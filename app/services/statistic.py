
import requests
from app.models import Post
from app import db
from datetime import datetime
from app.models import Statistics

import requests
from app.models import statistics
from app import db
from datetime import datetime

sorted_provinces = [
    "Hà Nội", "Hà Giang", "Cao Bằng", "Lai Châu", "Lào Cai", "Tuyên Quang", "Yên Bái", 
    "Điện Biên", "Bắc Kạn", "Lạng Sơn", "Bắc Giang", "Phú Thọ", "Quảng Ninh", "Thái Nguyên", 
    "Bắc Ninh", "Hải Dương", "Hải Phòng", "Hưng Yên", "Nam Định", "Ninh Bình", "Thái Bình", 
    "Vĩnh Phúc", "Đắk Lắk", "Gia Lai", "Kon Tum", "Lâm Đồng", "Bình Định", "Bình Thuận", 
    "Đà Nẵng", "Khánh Hòa", "Ninh Thuận", "Phú Yên", "Quảng Nam", "Quảng Ngãi", "Đắk Nông", 
    "Sóc Trăng", "Bà Rịa - Vũng Tàu", "Bình Dương", "Bình Phước", "Đồng Nai", "Tây Ninh", 
    "Hồ Chí Minh", "An Giang", "Bạc Liêu", "Bến Tre", "Cà Mau", "Đồng Tháp", "Long An", 
    "Tiền Giang", "Trà Vinh", "Vĩnh Long", "Hậu Giang", "Kiên Giang", "Cần Thơ", 
    "Nghệ An", "Hà Tĩnh", "Quảng Bình", "Quảng Trị", "Thanh Hóa", "Thừa Thiên - Huế"
]

def update_location_post_counts_from_api(api_url, headers=None, app=None):
    with app.app_context():
        # Update payload with corresponding time
        date_from = "2024/01/01 00:00:00"
        date_to = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        
        payload = {
            "date_from": date_from,
            "date_to": date_to,
            "topic_ids": None,
            "sentiment": None
        }

        try:
            response = requests.post(api_url, json=payload, headers=headers, verify=False)
            response.raise_for_status()  # Raise an HTTPError if the HTTP request returned an unsuccessful status code

            api_data = response.json()
            locations = api_data.get("data", {}).get("locations", [])

            # Map location names to IDs based on their order in sorted_provinces
            location_id_map = {loc: idx + 1 for idx, loc in enumerate(sorted_provinces)}

            for loc in locations:
                location_name = loc.get("location")
                if location_name in location_id_map:
                    location_id = location_id_map[location_name]
                    location_data = {
                        "id": location_id,
                        "location": location_name,
                        "total_count": loc.get("total_count"),
                        "positive_count": loc.get("positive_count"),
                        "neutral_count": loc.get("neutral_count"),
                        "negative_count": loc.get("negative_count"),
                    }

                    try:
                        existing_location = Statistics.query.filter_by(id=location_data["id"]).first()
                        if existing_location:
                            existing_location.total_count = location_data["total_count"]
                            existing_location.positive_count = location_data["positive_count"]
                            existing_location.neutral_count = location_data["neutral_count"]
                            existing_location.negative_count = location_data["negative_count"]
                        else:
                            new_location = Statistics(**location_data)
                            db.session.add(new_location)

                        db.session.commit()

                    except Exception as e:
                        db.session.rollback()
                        print(f"Error updating database: {e}")

        except requests.RequestException as e:
            print(f"API request failed: {e}")

        except ValueError as e:
            print(f"Error parsing JSON response: {e}")
