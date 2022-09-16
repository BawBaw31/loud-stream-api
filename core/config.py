from pydantic import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    app_name: str = "Loud Stream API"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
