from functools import lru_cache
import os

from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Loud Stream API"
    jwt_secret_key: str
    jwt_algorithm: str
    access_token_expire_minutes: int
    database_url: str
    aws_bucket_name: str

    class Config:
        environment = os.getenv("ENV", "production")
        env_file = ["sql_app/.env", "sql_app/.env.local",
                    f"sql_app/.env.{environment}"]
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings():
    return Settings()
