import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL', 'postgresql://postgres:Cm11_DiepNNTgzCg1166@10.32.118.11:5432/postgres')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PLATFORM_API_URL = os.getenv('PLATFORM_API_URL', 'http://192.168.20.20')
    SPYDER_API_URL = os.getenv('SPYDER_API_URL', 'http://example.com.vn')
    USERNAME_PLATFORM = os.getenv('USERNAME_PLATFORM', 'platform_username')
    PASSWORD_PLATFORM = os.getenv('PASSWORD_PLATFORM', 'platform_password')
    USERNAME_SPYDER = os.getenv('USERNAME_SPYDER', 'spyder_username')
    PASSWORD_SPYDER = os.getenv('PASSWORD_SPYDER', 'spyder_password')
    URL_SUPABASE = os.getenv('URL_SUPABASE', "http://127.0.0.1")
