import os
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = "sqlite:///notes.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "mysecretkey123456789012345678901234567890")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=30)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=7)