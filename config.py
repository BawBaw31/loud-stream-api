from pydantic import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    app_name: str = "Awesome API"
    # admin_email: str = ""
    items_per_user: int = 50

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
