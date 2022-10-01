from fastapi import APIRouter, Depends, File, Form, UploadFile
from fastapi.responses import StreamingResponse
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

    audio_file_name = storage.generate_file_name(
        "audio", audio_file.filename.split(".")[1], music_title, current_artist.stage_name)
    cover_file_name = storage.generate_file_name(
        "cover", cover_file.filename.split(".")[1], music_title, current_artist.stage_name)

    await storage.upload_file_to_s3(audio_file, audio_file_name)
    await storage.upload_file_to_s3(cover_file, cover_file_name)

    music_order = schemas.MusicOrder(
        title=music_title, genre=music_genre, audio_file_name=audio_file_name, cover_file_name=cover_file_name)

    return crud.create_music(db, music_order, current_artist.id)


@router.get("/", response_model=list[schemas.Music])
async def get_all_musics(db: Session = Depends(get_db)):

    return crud.get_musics(db)


@router.get("/{music_id}")
async def get_music(music_id: int, db: Session = Depends(get_db), storage: Storage = Depends(Storage)):

    music: schemas.Music = crud.get_music(db, music_id)
    return StreamingResponse(storage.download_music_from_s3(music.audio_file_name), media_type="music/mp3")
