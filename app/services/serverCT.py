import os
import json
from dotenv import load_dotenv
from app import db
from models import ServerCT
import requests
from sqlalchemy import select
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID, ARRAY
import uuid
import app

# Lấy API_URLS từ biến môi trường và chuyển thành dictionary
API_URLS = json.loads(os.getenv("API_URLS"))

def get_unit_id_manager(unit_name):
    stmt = select([db.Column('id')]).select_from(db.Table('unit', db.metadata, schema='btth')).where(db.Column('name') == unit_name)
    result = db.session.execute(stmt).fetchone()
    return result[0] if result else None

def update_server_status(app=None):
    with app.app_context():
        for unit_name, url in API_URLS.items():
            try:
                response = requests.get(url, timeout=10)
                status = "up" if response.status_code == 200 else "down"
                unit_id_manager = get_unit_id_manager(unit_name)
                if unit_id_manager:
                    server = db.session.query(ServerCT).filter_by(unit_id_manager=unit_id_manager).first()
                    if server:
                        server.status = status
                        server.last_up = datetime.utcnow()
                    else:
                        new_server = ServerCT(
                            uuid=str(uuid.uuid4()),
                            cpu=None,
                            unit_id_manager=unit_id_manager,
                            last_up=datetime.utcnow(),
                            ip=[],
                            status=status,
                            storage=None,
                            ram=None,
                            host_name=None
                        )
                        db.session.add(new_server)
                    db.session.commit()
                else:
                    print(f"Unit {unit_name} not found in the database.")

            except requests.exceptions.RequestException as e:
                print(f"Failed to connect to {url}: {e}")

