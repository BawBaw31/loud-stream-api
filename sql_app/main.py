from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import artists, musics
from .artists import main, models
from .core.database import engine
from .musics import main, models

artists.models.Base.metadata.create_all(bind=engine)
musics.models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(artists.main.router)
app.include_router(musics.main.router)
