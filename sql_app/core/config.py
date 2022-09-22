from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Loud Stream API"
    jwt_secret_key: str
    jwt_algorithm: str
    access_token_expire_minutes: int
    database_url: str
    aws_bucket_name: str

    class Config:
        env_file = "sql_app/.env"
        env_file_encoding = "utf-8"
