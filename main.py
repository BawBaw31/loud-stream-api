from functools import lru_cache

from core.config import Settings
from fastapi import FastAPI

import users.main

app = FastAPI()


@lru_cache()
def get_settings():
    return Settings()


app.include_router(users.main.router)
