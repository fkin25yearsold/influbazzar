from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "postgresql://neondb_owner:npg_Vj6SlOdKIPT8@ep-shy-lake-a1xucvko-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require"
    
    # JWT
    JWT_SECRET: str = "your-super-secret-jwt-key-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRY: int = 3600  # 1 hour
    
    # Email
    MAIL_FROM: str = "admin@influbazzar.com"
    MAIL_SERVER: str = "smtp.example.com"
    MAIL_PORT: int = 587
    MAIL_USERNAME: Optional[str] = None
    MAIL_PASSWORD: Optional[str] = None
    
    # Google OAuth
    GOOGLE_CLIENT_ID: Optional[str] = None
    
    class Config:
        env_file = "/app/.env"

settings = Settings()