import requests
from app.models import Statistics
from app import db
from datetime import datetime, timedelta

# Mã tỉnh theo danh sách bạn cung cấp
location_id_map = {
    "Hà Nội": 1, "Hà Giang": 2, "Cao Bằng": 4, "Bắc Kạn": 6, "Tuyên Quang": 8,
    "Lào Cai": 10, "Điện Biên": 11, "Lai Châu": 12, "Sơn La": 14, "Yên Bái": 15,
    "Hoà Bình": 17, "Thái Nguyên": 19, "Lạng Sơn": 20, "Quảng Ninh": 22, "Bắc Giang": 24,
    "Phú Thọ": 25, "Vĩnh Phúc": 26, "Bắc Ninh": 27, "Hải Dương": 30, "Hải Phòng": 31,
    "Hưng Yên": 33, "Thái Bình": 34, "Hà Nam": 35, "Nam Định": 36, "Ninh Bình": 37,
    "Thanh Hóa": 38, "Nghệ An": 40, "Hà Tĩnh": 42, "Quảng Bình": 44, "Quảng Trị": 45,
    "Thừa Thiên Huế": 46, "Đà Nẵng": 48, "Quảng Nam": 49, "Quảng Ngãi": 51, "Bình Định": 52,
    "Phú Yên": 54, "Khánh Hòa": 56, "Ninh Thuận": 58, "Bình Thuận": 60, "Kon Tum": 62,
    "Gia Lai": 64, "Đắk Lắk": 66, "Đắk Nông": 67, "Lâm Đồng": 68, "Bình Phước": 70,
    "Tây Ninh": 72, "Bình Dương": 74, "Đồng Nai": 75, "Bà Rịa - Vũng Tàu": 77,
    "TP Hồ Chí Minh": 79, "Long An": 80, "Tiền Giang": 82, "Bến Tre": 83,
    "Trà Vinh": 84, "Vĩnh Long": 86, "Đồng Tháp": 87, "An Giang": 89,
    "Kiên Giang": 91, "Cần Thơ": 92, "Hậu Giang": 93, "Sóc Trăng": 94,
    "Bạc Liêu": 95, "Cà Mau": 96
}

def update_location_post_counts_from_api(api_url, headers=None, app=None):
    with app.app_context():
        # Tính toán thời gian cho date_from và date_to
        date_to = datetime.now()
        date_from = date_to - timedelta(days=7)

        # Định dạng thời gian
        date_from_str = date_from.strftime("%Y/%m/%d %H:%M:%S")
        date_to_str = date_to.strftime("%Y/%m/%d %H:%M:%S")

        payload = {
            "date_from": date_from_str,
            "date_to": date_to_str,
            "topic_ids": None,
            "sentiment": None
        }

        try:
            response = requests.post(api_url, json=payload, headers=headers, verify=False)
            response.raise_for_status()

            api_data = response.json()
            locations = api_data.get("data", {}).get("locations", [])

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
