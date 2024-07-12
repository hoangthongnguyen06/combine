import os
from dotenv import load_dotenv

load_dotenv()
class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://username:password@localhost/dbname')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PLATFORM_API_URL = os.getenv('PLATFORM_API_URL', 'http://192.168.20.20')
    SPYDER_API_URL = os.getenv('SPYDER_API_URL', 'http://example.com.vn')
