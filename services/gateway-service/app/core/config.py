import os
from pathlib import Path
from typing import List
from dotenv import load_dotenv
import json

# Load the .env file from 2 levels up: /app/core/config.py → /gateway-service/.env
env_path = Path(__file__).resolve().parents[2] / ".env"

load_dotenv(dotenv_path=env_path, override=True)

class Settings:
    # Common settings
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "local")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here-change-in-production")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    REFRESH_TOKEN_EXPIRE_DAYS: int = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))
    
    APP_NAME: str = os.getenv("APP_NAME", "Sehat-Iqra Gateway Service")
    PROJECT_NAME: str = os.getenv("PROJECT_NAME", "Sehat-Iqra Gateway Service")
    API_V1_STR: str = os.getenv("API_V1_STR", "/api/v1")
    
    # Service URLs
    AUTH_SERVICE_URL: str = os.getenv("AUTH_SERVICE_URL", "http://auth-service:8000")
    HOSPITAL_SERVICE_URL: str = os.getenv("HOSPITAL_SERVICE_URL", "http://hospital-service:8000")
    RESOURCE_SERVICE_URL: str = os.getenv("RESOURCE_SERVICE_URL", "http://resource-service:8000")
    BLOOD_SERVICE_URL: str = os.getenv("BLOOD_SERVICE_URL", "http://blood-service:8000")
    NGO_SERVICE_URL: str = os.getenv("NGO_SERVICE_URL", "http://ngo-service:8000")
    NOTIFICATION_SERVICE_URL: str = os.getenv("NOTIFICATION_SERVICE_URL", "http://notification-service:8000")
    AI_SERVICE_URL: str = os.getenv("AI_SERVICE_URL", "http://ai-service:8000")
    
    # CORS settings
    _BACKEND_CORS_ORIGINS = os.getenv("BACKEND_CORS_ORIGINS", '["http://localhost:5173", "http://127.0.0.1:5173"]')
    
    @property
    def BACKEND_CORS_ORIGINS(self) -> List[str]:
        try:
            return json.loads(self._BACKEND_CORS_ORIGINS)
        except:
            return ["http://localhost:5173", "http://127.0.0.1:5173"]

    class Config:
        case_sensitive = True

settings = Settings()
