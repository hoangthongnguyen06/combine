# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.config import Config
import requests

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)

    # Import các models ở đây để đảm bảo các bảng được tạo khi chạy db.create_all()
    from app.models import post, domain, author, unit, nuance, topic, hashtag
    
    with app.app_context():
        db.create_all()
    
    return app
