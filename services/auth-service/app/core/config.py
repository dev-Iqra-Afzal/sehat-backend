import os
from enum import Enum
from pathlib import Path

from dotenv import load_dotenv
from pydantic import SecretStr
from pydantic_settings import BaseSettings

# Load the .env file from 2 levels up: /app/core/config.py → /resource-service/.env
env_path = Path(__file__).resolve().parents[2] / ".env"

load_dotenv(dotenv_path=env_path, override=True)

# -----------------------------------------
#               SETTINGS CLASSES
# -----------------------------------------

class AppSettings(BaseSettings):
    APP_NAME: str = os.getenv("APP_NAME", "Auth Service")
    APP_DESCRIPTION: str | None = os.getenv("APP_DESCRIPTION")
    APP_VERSION: str | None = os.getenv("APP_VERSION")
    LICENSE_NAME: str | None = os.getenv("LICENSE")
    CONTACT_NAME: str | None = os.getenv("CONTACT_NAME")
    CONTACT_EMAIL: str | None = os.getenv("CONTACT_EMAIL")


class CryptSettings(BaseSettings):
    SECRET_KEY: SecretStr = SecretStr(os.getenv("SECRET_KEY"))
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
    REFRESH_TOKEN_EXPIRE_DAYS: int = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", 7))


class DatabaseSettings(BaseSettings):
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "auth_user")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER", "postgres")
    POSTGRES_PORT: int = int(os.getenv("POSTGRES_PORT", 5432))
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "auth_db")
    POSTGRES_SYNC_PREFIX: str = os.getenv("POSTGRES_SYNC_PREFIX", "postgresql://")
    POSTGRES_ASYNC_PREFIX: str = os.getenv("POSTGRES_ASYNC_PREFIX", "postgresql+asyncpg://")
    POSTGRES_URL: str | None = os.getenv("POSTGRES_URL")

    @property
    def POSTGRES_URI(self) -> str:
        return f"{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"


class RedisCacheSettings(BaseSettings):
    REDIS_CACHE_HOST: str = os.getenv("REDIS_CACHE_HOST", "localhost")
    REDIS_CACHE_PORT: int = int(os.getenv("REDIS_CACHE_PORT", 6379))

    # Flat field for Redis URL
    @property
    def REDIS_CACHE_URL(self) -> str:
        return f"redis://{self.REDIS_CACHE_HOST}:{self.REDIS_CACHE_PORT}"

    # REDIS_CACHE_URL: str = f"redis://{os.getenv('REDIS_CACHE_HOST', 'localhost')}:{os.getenv('REDIS_CACHE_PORT', '6379')}"


class RedisQueueSettings(BaseSettings):
    REDIS_QUEUE_HOST: str = os.getenv("REDIS_QUEUE_HOST", "localhost")
    REDIS_QUEUE_PORT: int = int(os.getenv("REDIS_QUEUE_PORT", 6379))

    @property
    def REDIS_CACHE_URL(self) -> str:
        return f"redis://{self.REDIS_CACHE_HOST}:{self.REDIS_CACHE_PORT}"


class RabbitMQSettings(BaseSettings):
    RABBITMQ_HOST: str = os.getenv("RABBITMQ_HOST", "localhost")
    RABBITMQ_PORT: int = int(os.getenv("RABBITMQ_PORT", 5672))
    RABBITMQ_USER: str = os.getenv("RABBITMQ_USER", "guest")
    RABBITMQ_PASSWORD: str = os.getenv("RABBITMQ_PASSWORD", "guest")
    
    @property
    def RABBITMQ_URL(self) -> str:
        return f"amqp://{self.RABBITMQ_USER}:{self.RABBITMQ_PASSWORD}@{self.RABBITMQ_HOST}:{self.RABBITMQ_PORT}/"


class EnvironmentOption(Enum):
    LOCAL = "local"
    STAGING = "staging"
    PRODUCTION = "production"


class EnvironmentSettings(BaseSettings):
    ENVIRONMENT: EnvironmentOption = EnvironmentOption(os.getenv("ENVIRONMENT", "local"))

# -----------------------------------------
#           COMBINED SETTINGS
# -----------------------------------------

class Settings(
    AppSettings,
    DatabaseSettings,
    CryptSettings,
    RedisQueueSettings,
    RabbitMQSettings,
    EnvironmentSettings,
    RedisCacheSettings
):
    pass


# Instantiate once and import from anywhere
settings = Settings()
