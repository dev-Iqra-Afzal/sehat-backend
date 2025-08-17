import os  # Module for interacting with the OS
from enum import Enum  # For defining constant values
from pathlib import Path  # For handling filesystem paths

from dotenv import load_dotenv  # Load environment variables from a .env file
from pydantic import SecretStr  # Securely handle sensitive info like passwords or API keys
from pydantic_settings import BaseSettings  # Define settings classes with validation

# Load the .env file from a specific path
env_path = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(dotenv_path=env_path, override=True)

class AppSettings(BaseSettings):
    APP_NAME: str = os.getenv("APP_NAME", "Notification Service")
    APP_DESCRIPTION: str | None = os.getenv("APP_DESCRIPTION")
    APP_VERSION: str | None = os.getenv("APP_VERSION")
    LICENSE_NAME: str | None = os.getenv("LICENSE")
    CONTACT_NAME: str | None = os.getenv("CONTACT_NAME")
    CONTACT_EMAIL: str | None = os.getenv("CONTACT_EMAIL")


class CryptSettings(BaseSettings):
    SECRET_KEY: SecretStr = SecretStr(os.getenv("SECRET_KEY", "dev-secret"))
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
    REFRESH_TOKEN_EXPIRE_DAYS: int = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", 7))


class DatabaseSettings(BaseSettings):
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "notification_user")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "notification_db_password")
    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER", "postgres")
    POSTGRES_PORT: int = int(os.getenv("POSTGRES_PORT", 5432))
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "resource_db")
    POSTGRES_SYNC_PREFIX: str = os.getenv("POSTGRES_SYNC_PREFIX", "postgresql://")
    POSTGRES_ASYNC_PREFIX: str = os.getenv("POSTGRES_ASYNC_PREFIX", "postgresql+asyncpg://")
    POSTGRES_URL: str | None = os.getenv("POSTGRES_URL")
    
    @property
    def POSTGRES_URI(self) -> str:
        return f"{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"


class RedisCacheSettings(BaseSettings):
    REDIS_CACHE_HOST: str = os.getenv("REDIS_CACHE_HOST", "localhost")
    REDIS_CACHE_PORT: int = int(os.getenv("REDIS_CACHE_PORT", 6379))
    
    @property
    def REDIS_CACHE_URL(self) -> str:
        return f"redis://{self.REDIS_CACHE_HOST}:{self.REDIS_CACHE_PORT}"


class RedisQueueSettings(BaseSettings):
    REDIS_QUEUE_HOST: str = os.getenv("REDIS_QUEUE_HOST", "localhost")
    REDIS_QUEUE_PORT: int = int(os.getenv("REDIS_QUEUE_PORT", 6379))


class EnvironmentOption(Enum):
    LOCAL = "local"
    STAGING = "staging"
    PRODUCTION = "production"


class EnvironmentSettings(BaseSettings):
    ENVIRONMENT: EnvironmentOption = EnvironmentOption(os.getenv("ENVIRONMENT", "local"))


# Combine all settings into one
class Settings(
    AppSettings,
    DatabaseSettings,
    CryptSettings,
    RedisQueueSettings,
    EnvironmentSettings,
):
    pass

# Load settings
settings = Settings()
