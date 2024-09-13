import os
import json
from dotenv import load_dotenv
from app import db
from app.models import ServerCT
import requests
from sqlalchemy import select
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID, ARRAY
import uuid
import app
from sqlalchemy import text
# Lấy API_URLS từ biến môi trường và chuyển thành dictionary
API_URLS = json.loads(os.getenv("API_URLS"))

def get_unit_id_manager(unit_name):
    # Truy vấn unit_id_manager bằng cách sử dụng câu lệnh SQL trực tiếp
    result = db.session.execute(
        text('SELECT id FROM "btth"."unit" WHERE name = :name'),
        {'name': unit_name}
    )
    unit_id_manager = result.fetchone()
    return unit_id_manager[0] if unit_id_manager else None

from sqlalchemy.dialects.postgresql import UUID
import uuid

def update_server_status(app=None):
    with app.app_context():
        for unit_name, url in API_URLS.items():
            try:
                # response = requests.get(url, timeout=60)
                # status = "up" if response.status_code == 200 else "down"
                status = "up"
                unit_id_manager = get_unit_id_manager(unit_name)
                if unit_id_manager:
                    # Xử lý cho hai máy chủ với các IP cụ thể
                    for ip in ["10.16.69.202", "10.16.69.203"]:
                        server = db.session.query(ServerCT).filter_by(name=unit_name, ip=ip).first()
                        if server:
                            server.status = status
                            server.added_to_json="2",
                            server.last_up = datetime.utcnow()
                        else:
                            new_server = ServerCT(
                                uuid=uuid.uuid4(),
                                cpu=None,
                                unit_id_manager=str(unit_id_manager),
                                last_up=datetime.utcnow(),
                                ip=ip,
                                status=status,
                                storage=None,
                                added_to_json="1",
                                ram=None,
                                host_name=None,
                                name=unit_name
                            )
                            db.session.add(new_server)
                    
                    db.session.commit()
                else:
                    print(f"Unit {unit_name} not found in the database.")

            except requests.exceptions.RequestException as e:
                print(f"Failed to connect to {url}: {e}")