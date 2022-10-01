from fastapi import APIRouter, Depends, File, Form, UploadFile
from sql_app.artists.schemas import Artist
from sql_app.core.database import get_db
from sql_app.core.dependencies import get_current_artist
from sql_app.core.storage import Storage
from sql_app.musics import crud
from sqlalchemy.orm import Session

from . import schemas

router = APIRouter(
    prefix="/musics",
    tags=["musics"],
)


@router.post("/", response_model=schemas.Music)
async def add_music(audio_file: UploadFile = File(...), cover_file: UploadFile = File(...),
                    music_title: str = Form(...), music_genre: schemas.GenresEnum = Form(...),
                    db: Session = Depends(get_db), current_artist: Artist = Depends(get_current_artist),
                    storage: Storage = Depends(Storage)):
    music_order = schemas.MusicOrder(
        title=music_title, genre=music_genre, audio_file=audio_file, cover_file=cover_file)
    return crud.create_music(db, music_order, current_artist, storage)


@router.get("/", response_model=list[schemas.Music])
async def get_all_musics(db: Session = Depends(get_db)):
    return crud.get_musics(db)


@router.get("/{music_id}", response_model=schemas.Music)
async def get_music(music_id: int, db: Session = Depends(get_db)):
    return crud.get_music(db, music_id)
