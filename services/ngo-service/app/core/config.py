import os   # it is a module that provides a way to use operating system dependent functionality like reading or writing to the file system.
from enum import Enum   # Used to define et of values that can be used as contants

# A python module that provides a way to define settings for an application using Pydantic.
# Load config values from .env files or OS environment variables.
# Automatically convert them to the right types (int, bool, str, etc.).
from pydantic_settings import BaseSettings 

from pydantic import SecretStr  # Used to handle sensitive information like passwords or API keys securely

from starlette.config import Config  # used to read configuration from environment variables or .env files

from pathlib import Path  # A module to handle filesystem paths in a platform-independent way

# __file__
# This is a special built-in variable in Python. It holds the path to the current file
# .parent # This is a property of the Path object that returns the parent directories of the current file
# .resolve() # This method resolves the path to an absolute path, following any symbolic links
env_path = Path(__file__).resolve().parent / '.env'

# Create a Config object with the resolved .env file
config = Config(env_path)

class AppSettings(BaseSettings):
    APP_NAME: str = config("APP_NAME", default="NGO Service")
    APP_DESCRIPTION: str | None = config("APP_DESCRIPTION", default=None)
    APP_VERSION: str | None = config("APP_VERSION", default=None)
    LICENSE_NAME: str | None = config("LICENSE", default=None)
    CONTACT_NAME: str | None = config("CONTACT_NAME", default=None)
    CONTACT_EMAIL: str | None = config("CONTACT_EMAIL", default=None)

class CryptSettings(BaseSettings):
    SECRET_KEY: SecretStr = config("SECRET_KEY", cast=SecretStr, default="dev-secret")
    ALGORITHM: str = config("ALGORITHM", default="HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = config("ACCESS_TOKEN_EXPIRE_MINUTES", default=30)
    REFRESH_TOKEN_EXPIRE_DAYS: int = config("REFRESH_TOKEN_EXPIRE_DAYS", default=7)

class EnvironmentOption(Enum):
    LOCAL = "local"
    STAGING = "staging"
    PRODUCTION = "production"


class EnvironmentSettings(BaseSettings):
    ENVIRONMENT: EnvironmentOption = config("ENVIRONMENT", default=EnvironmentOption.LOCAL)

# Combines all the config classes into one unified Settings object for centralized access.
class Settings(
    AppSettings,
    CryptSettings,
    EnvironmentSettings,
):
    pass

# Instantiates Settings, which automatically loads all environment variables from .env via all the inherited classes.
settings = Settings()
