import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://postgres:Cm11_DiepNNTgzCg1166@10.32.118.11:5432/postgres')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PLATFORM_API_URL = os.getenv('PLATFORM_API_URL', 'http://192.168.20.20')
    SPYDER_API_URL = os.getenv('SPYDER_API_URL', 'https://app.spyder.internal')
    USERNAME_PLATFORM = os.getenv('USERNAME_PLATFORM', 'username')
    PASSWORD_PLATFORM = os.getenv('PASSWORD_PLATFORM', 'password')

    
