
import requests
from app.models import Post
from app import db
from datetime import datetime
from app.models import Channel

import requests
from app.models import channel
from app import db
from datetime import datetime

def fetch_channel_data_from_api(api_url, headers=None, app=None):
    with app.app_context():
        try:
            response = requests.get(api_url, headers=headers, verify=False)
            response.raise_for_status()  # Raise an HTTPError if the HTTP request returned an unsuccessful status code

            api_data = response.json()
            channels = api_data.get("data", {}).get("channels", [])

            for ch in channels:
                channel_data = {
                    "id": ch.get("id"),
                    "name": ch.get("name"),
                    "type": ch.get("type"),
                    "url": ch.get("url"),
                    "total_post": ch.get("total_post"),
                    "created_by_id": ch.get("created_by_id"),
                    "created_at": ch.get("created_at"),
                }

                try:
                    existing_channel = Channel.query.filter_by(id=channel_data["id"]).first()
                    if existing_channel:
                        existing_channel.name = channel_data["name"]
                        existing_channel.type = channel_data["type"]
                        existing_channel.url = channel_data["url"]
                        existing_channel.total_post = channel_data["total_post"]
                        existing_channel.created_by_id = channel_data["created_by_id"]
                        existing_channel.created_at = datetime.strptime(channel_data["created_at"], '%Y/%m/%d %H:%M:%S')
                    else:
                        new_channel = Channel(**channel_data)
                        db.session.add(new_channel)

                    db.session.commit()

                except Exception as e:
                    db.session.rollback()
                    print(f"Error updating database: {e}")

        except requests.RequestException as e:
            print(f"API request failed: {e}")

        except ValueError as e:
            print(f"Error parsing JSON response: {e}")