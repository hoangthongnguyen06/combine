from datetime import datetime
from app.models import BotCT86
import requests
import os
import json
from app import db
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy import text

def get_unit_id(unit_name: str) -> str:
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

def fetch_and_update_bot_data(app=None):
    with app.app_context():
        # Read API_URLS from .env
        api_urls_str = os.getenv('API_URLS')
        
        if api_urls_str is None:
            raise ValueError("API_URLS environment variable is not set or is None")
        
        try:
            api_urls = json.loads(api_urls_str)
        except json.JSONDecodeError as e:
            raise ValueError(f"API_URLS environment variable is not a valid JSON string: {e}")
        
        # Loop through each unit_name and api_url
        for unit_name, api_url in api_urls.items():
            try:
                # Call API and get data
                response = requests.get(api_url)
                response.raise_for_status()
                
                api_data = response.json()
                
                # Get unit_id only once per unit_name
                unit_id = get_unit_id(unit_name)
                
                if unit_id is None:
                    print(f"Không tìm thấy đơn vị với tên: {unit_name}")
                    continue
                
                # Update bot data
                update_bot_data_from_api(api_data, unit_id)
            except requests.RequestException as e:
                print(f"Failed to fetch data from {api_url} for {unit_name}. Error: {e}")

def update_bot_data_from_api(api_data, unit_id):
    try:
        fb_account_details = api_data.get('items', [])[0].get('FB_Account_Detail', [])
        
        for account in fb_account_details:
            bot = BotCT86(
                email=account.get('email'),
                uid=str(account.get('uuid')),
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
                status=account.get('status'),
                unit_id=unit_id,  # Use the fetched unit_id
                added_to_json="1"
            )
            
            existing_bot = BotCT86.query.filter_by(uid=bot.uid).first()
            
            if existing_bot:
                existing_bot.updated_at = datetime.utcnow()
                existing_bot.added_to_json="2"
                db.session.commit()
            else:
                db.session.add(bot)
                db.session.commit()

    except Exception as e:
        print(f"Error updating bot data: {e}")
        db.session.rollback()
