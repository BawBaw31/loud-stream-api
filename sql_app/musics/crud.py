from sqlalchemy.orm import Session

from sql_app.core.storage import Storage

from ..artists import schemas as artist_schemas
from . import models, schemas


def get_music(db: Session, music_id: int):
    return db.query(models.Music).filter(models.Music.id == music_id).first()


def get_music_by_title(db: Session, music_title: str):
    return db.query(models.Music).filter(models.Music.email == music_title).first()


def get_musics(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Music).offset(skip).limit(limit).all()


def create_music(db: Session, music_order: schemas.MusicOrder, owner: artist_schemas.Artist, storage: Storage) -> schemas.Music:
    uploaded_audio_file_url = storage.upload_file_to_s3(music_order.audio_file)
    uploaded_cover_img_url = storage.upload_file_to_s3(music_order.cover_file)

    db_music = models.Music(title=music_order.title, genre=music_order.genre._value_,
                            audio_file_url=uploaded_audio_file_url, cover_img_url=uploaded_cover_img_url, owner_id=owner.id)

    db.add(db_music)
    db.commit()
    db.refresh(db_music)

    return db_music
