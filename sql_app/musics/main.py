from fastapi import APIRouter, Depends
from sql_app.artists.schemas import Artist
from sql_app.core.dependencies import get_current_artist, get_db
from sql_app.musics import crud
from sqlalchemy.orm import Session

from . import schemas

router = APIRouter(
    prefix="/musics",
    tags=["musics"],
)


@router.post("/", response_model=schemas.Music)
async def upload_music(music: schemas.MusicBase, db: Session = Depends(get_db), current_artist: Artist = Depends(get_current_artist)):
    music_create = schemas.MusicCreate(
        **music.dict(), owner_id=current_artist.id)
    return crud.create_music(db, music_create)


@router.get("/", response_model=list[schemas.Music])
async def get_all_musics(db: Session = Depends(get_db)):
    return crud.get_musics(db)


@router.get("/{music_id}", response_model=schemas.Music)
async def get_music_by_id(music_id: int, db: Session = Depends(get_db)):
    return crud.get_music(db, music_id)


@router.get("/{music_title}", response_model=schemas.Music)
async def get_music_by_title(music_title: str, db: Session = Depends(get_db)):
    return crud.get_music_by_title(db, music_title)
