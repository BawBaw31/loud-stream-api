from sqlalchemy.orm import Session

from . import models, schemas


def get_music(db: Session, music_id: int):
    return db.query(models.Music).filter(models.Music.id == music_id).first()


def get_musics(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Music).offset(skip).limit(limit).all()


def create_music(db: Session, music_order: schemas.MusicOrder, owner_id: int) -> schemas.Music:
    db_music = models.Music(title=music_order.title, genre=music_order.genre._value_,
                            audio_file_name=music_order.audio_file_name, cover_file_name=music_order.cover_file_name,
                            owner_id=owner_id)

    db.add(db_music)
    db.commit()
    db.refresh(db_music)

    return db_music
