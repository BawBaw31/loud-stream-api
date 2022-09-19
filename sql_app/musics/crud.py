from sql_app.artists.crud import get_artist
from sqlalchemy.orm import Session

from . import models, schemas


def get_music(db: Session, music_id: int):
    return db.query(models.Music).filter(models.Music.id == music_id).first()


def get_music_by_title(db: Session, music_title: str):
    return db.query(models.Music).filter(models.Music.email == music_title).first()


def get_musics(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Music).offset(skip).limit(limit).all()


def create_music(db: Session, music: schemas.MusicCreate):
    db_music = models.Music(title=music.title, audio_file_url=music.audio_file_url, cover_img_url=music.cover_img_url,
                            genre=music.genre._value_, owner_id=music.owner.id)
    db.add(db_music)
    for collaborator_id in music.collaborators_ids:
        if collaborator_id != music.owner.id:
            db_music.collaborators.append(get_artist(db, collaborator_id))
    db.commit()
    db.refresh(db_music)
    return db_music
