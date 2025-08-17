import os   # it is a module that provides a way to use operating system dependent functionality like reading or writing to the file system.
from enum import Enum   # Used to define et of values that can be used as contants

# A python module that provides a way to define settings for an application using Pydantic.
# Automatically convert them to the right types (int, bool, str, etc.). as .env varibales are all strings
from pydantic_settings import BaseSettings 
# Used to handle sensitive information like passwords or API keys securely. It is accessible via .get_secret_value()
# so when this is displayed, only **** are printed instead of actual value 
from pydantic import SecretStr  
from pathlib import Path  # A module to handle filesystem paths in a platform-independent way
# It’s a third-party Python package (not built into Python) that helps you 
# load environment variables from a file named .env into your program’s environment.
from dotenv import load_dotenv

# __file__
# This is a special built-in variable in Python. It holds the path to the current file
# .resolve() # This method resolves the path to an absolute path, following any symbolic links
# .parent # This is a property of the Path object that returns the parent directories of the current file
# Load the .env file from 2 levels up: /app/core/config.py → /resource-service/.env
env_path = Path(__file__).resolve().parents[2] / ".env"

load_dotenv(dotenv_path=env_path, override=True)


OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

HF_API_KEY = os.getenv("HF_API_KEY")
HF_MODEL = os.getenv("HF_MODEL")

GROQ_API_KEY = os.getenv("GROQ_API_KEY")


class AppSettings(BaseSettings):
    APP_NAME: str = os.getenv("APP_NAME", "AI Service")
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


class EnvironmentOption(Enum):
    LOCAL = "local"
    STAGING = "staging"
    PRODUCTION = "production"


class EnvironmentSettings(BaseSettings):
    ENVIRONMENT: EnvironmentOption = EnvironmentOption(os.getenv("ENVIRONMENT", "local"))

# Combines all the config classes into one unified Settings object for centralized access.
class Settings(
    AppSettings,
    CryptSettings,
    EnvironmentSettings,
):
    pass

# Instantiates Settings, which automatically loads all environment variables from .env via all the inherited classes.
settings = Settings()
