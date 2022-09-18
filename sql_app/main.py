from fastapi import FastAPI

from . import artists, musics
from .artists import main, models
from .core.database import engine
from .musics import main, models

artists.models.Base.metadata.create_all(bind=engine)
musics.models.Base.metadata.create_all(bind=engine)

app = FastAPI()


app.include_router(artists.main.router)
app.include_router(musics.main.router)
