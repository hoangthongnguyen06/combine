# update_service.py

from datetime import datetime
from app.models import Target 
import requests
import os
import json
from app import db
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy import text

# from app import db
def get_manage_unit_id(unit_name: str) -> str:
    try:
        result = db.session.execute(
            text('SELECT id FROM "TCTT_DonVi" WHERE name = :name'),
            {'name': unit_name}
        )
        unit_id = result.fetchone()
        return unit_id[0] if unit_id else None
    except Exception as e:
        print(f"Error fetching unit ID: {e}")
        return None
    
def get_platform_id(platform_name: str) -> str:
    result = db.session.execute(
            text('SELECT id FROM "TCTT_NenTang" WHERE name = :name'),
            {'name': platform_name}
    )
    platform_id = result.fetchone()
    return platform_id[0] if platform_id else None

def get_name_platform(template: str) -> str:
    if template == "fb_wall":
        return "Facebook"
    elif template == "youtube_wall":
        return "Youtube"
    elif template == "page":
        return "Các trang báo điện tử"
    else:
        return "unknown"

def update_target_from_api_data(api_data, manage_unit):
    for item in api_data['items']:
        source_unit_details = item.get('Source_Unit_Detail', [])

        for source_unit in source_unit_details:
            details = source_unit.get('details', [])
            unit = source_unit.get('project_name')
            
            for detail_list in details:
                for detail in detail_list:
                    target = Target(
                        created_at=datetime.utcnow(),
                        avatar=None,
                        image=None,
                        name=detail.get('name', None),
                        status="active",
                        nuance="default",
                        added_to_json="1",
                        name_platform=get_name_platform(detail.get('template', '')),
                        id_platform=get_platform_id(get_name_platform(detail.get('template', ''))),
                        keyword=[],
                        note="",
                        id_object=detail.get('social_id', None),
                        unit = unit,
                        manage_unit = get_manage_unit_id(unit_name=manage_unit)
                    )
                    existing_target = Target.query.filter_by(id_object=target.id_object).first()
                    
                    if existing_target:
                        existing_target.added_to_json = "2"
                        db.session.commit()
                        # print(f"Updated Target with ID: {existing_target.id_object}")
                    else:
                        db.session.add(target)
                        db.session.commit()
                        # print(f"Added Target with ID: {target.id_object}")

def fetch_and_update_data_target(app=None):
    with app.app_context():
        api_urls_str = os.getenv('API_URLS')
        
        if api_urls_str is None:
            raise ValueError("API_URLS environment variable is not set or is None")
        
        # print(f"Raw API_URLS: {api_urls_str}")
        
        try:
            api_urls = json.loads(api_urls_str)
        except json.JSONDecodeError as e:
            raise ValueError(f"API_URLS environment variable is not a valid JSON string: {e}")
        
        # print(f"Parsed API_URLS: {api_urls}")
        
        for key, url in api_urls.items():
            print(f"Fetching data from {key}: {url}")
            response = requests.get(url)

            if response.status_code == 200:
                api_data = response.json()
                update_target_from_api_data(api_data, key)
            else:
                print(f"Failed to fetch data from {url}, status code: {response.status_code}")
