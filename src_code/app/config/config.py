import re
from pathlib import Path
from dotenv import load_dotenv, set_key
from pydantic_settings import BaseSettings


ENV_FILE = ".env"
# Define paths
BASE_DIR = Path(__file__).resolve().parent.parent.parent  # Adjust if needed
VERSION_FILE = BASE_DIR /"VERSION.txt"


def get_latest_version():
    if VERSION_FILE.exists():
        with open(VERSION_FILE, "r") as file:
            content = file.read()
        # Find all semantic versions like 1.00.04
        matches = re.findall(r"APAAR API (\d+\.\d+\.\d+)", content)

        if matches:
            # Sort versions using tuple comparison
            versions = sorted(matches, key=lambda v: tuple(map(int, v.split('.'))), reverse=True)
            return versions[0]

    return "Unknown"

# Update .env or print
latest_version = get_latest_version()

# If a valid version is found, update the .env file
if latest_version != "Unknown":
    set_key(str(ENV_FILE), "APP_VERSION", latest_version)

# 🔹 Load .env AGAIN to reflect updates made by `set_key()`
load_dotenv(dotenv_path=str(ENV_FILE), override=True)

# Pydantic settings class
class Settings(BaseSettings):
    APP_NAME: str
    APP_VERSION: str
    APP_ENV: str
    APP_KEY: str
    APP_DEBUG: bool = False
    APP_TIMEZONE: str
    APP_URL: str
    ALLOW_ORIGINS: str
    
    
    
    # JWT Auth Configurations
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    JWT_TOKEN_EXPIRE_MINUTES: int = 30
    
    class Config:
        env_file = str(ENV_FILE)
        extra = "allow"

# Instantiate settings
settings = Settings()