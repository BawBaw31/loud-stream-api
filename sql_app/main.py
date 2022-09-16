from fastapi import FastAPI

from . import users
from .core.database import engine
from .users import main, models

users.models.Base.metadata.create_all(bind=engine)

app = FastAPI()


app.include_router(users.main.router)
