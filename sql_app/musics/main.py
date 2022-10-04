import pathlib

from fastapi import (APIRouter, Depends, File, Form, HTTPException, UploadFile,
                     status)
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from ..artists.schemas import Artist
from ..core.database import get_db
from ..core.dependencies import get_current_artist
from ..core.storage import Storage
from . import crud, schemas

router = APIRouter(
    prefix="/musics",
    tags=["musics"],
)


@router.post("/", response_model=schemas.Music)
async def add_music(audio_file: UploadFile = File(...), cover_file: UploadFile = File(...),
                    music_title: str = Form(...), music_genre: schemas.GenresEnum = Form(...),
                    db: Session = Depends(get_db), current_artist: Artist = Depends(get_current_artist),
                    storage: Storage = Depends(Storage)):

    errors = {}
    if audio_file.content_type != "audio/mpeg" and audio_file.content_type != "audio/wav":
        errors["audio_file"] = "Audio file must be mp3 or wav"
    if cover_file.content_type != "image/jpeg" and cover_file.content_type != "image/png":
        errors["cover_file"] = "Cover file must be jpeg or png"

    if len(errors.keys()):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=errors)

    audio_file_name = storage.generate_file_name(
        "audio", pathlib.Path(audio_file.filename).suffix, music_title, current_artist.stage_name)
    cover_file_name = storage.generate_file_name(
        "cover", pathlib.Path(cover_file.filename).suffix, music_title, current_artist.stage_name)

    await storage.upload_file_to_s3(audio_file, audio_file_name)
    await storage.upload_file_to_s3(cover_file, cover_file_name)

    music_order = schemas.MusicOrder(
        title=music_title, genre=music_genre, audio_file_name=audio_file_name, cover_file_name=cover_file_name)

    return crud.create_music(db, music_order, current_artist.id)


@router.get("/", response_model=list[schemas.Music])
async def get_all_musics(db: Session = Depends(get_db)):

    return crud.get_musics(db)


@router.get("/{music_id}")
async def stream_music_by_id(music_id: int, db: Session = Depends(get_db), storage: Storage = Depends(Storage)):

    music: schemas.Music = crud.get_music(db, music_id)
    media_type = "audio/mpeg" if music.audio_file_name.endswith(
        ".mp3") else "audio/wav"
    return StreamingResponse(storage.download_music_from_s3(music.audio_file_name), media_type=media_type)
