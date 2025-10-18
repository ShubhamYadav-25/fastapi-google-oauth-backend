import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings 

load_dotenv()

class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv('DATABASE_URL')
    GOOGLE_CLIENT_ID: str = os.getenv('GOOGLE_CLIENT_ID')
    GOOGLE_CLIENT_SECRET: str = os.getenv('GOOGLE_CLIENT_SECRET')
    JWT_SECRET_KEY: str = os.getenv('JWT_SECRET_KEY')
    ACCESS_TOKEN_EXPIRE_MINUTES: int = os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES')
    REFRESH_TOKEN_EXPIRE_DAYS: int = os.getenv('REFRESH_TOKEN_EXPIRE_DAYS')
    RATE_LIMIT: int = os.getenv('RATE_LIMIT')  # requests per minute
    CORS_ORIGINS: list = os.getenv('CORS_ORIGINS')

settings = Settings()
