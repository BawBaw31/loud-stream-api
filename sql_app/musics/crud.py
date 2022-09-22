import boto3
from fastapi import UploadFile
from sqlalchemy.orm import Session

from ..artists import schemas as artist_schemas
from . import models, schemas


def get_music(db: Session, music_id: int):
    return db.query(models.Music).filter(models.Music.id == music_id).first()


def get_music_by_title(db: Session, music_title: str):
    return db.query(models.Music).filter(models.Music.email == music_title).first()


def get_musics(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Music).offset(skip).limit(limit).all()


def upload_file_to_s3(file: UploadFile, bucket_name: str) -> str:
    s3 = boto3.resource("s3")
    bucket = s3.Bucket(bucket_name)
    try:
        bucket.upload_fileobj(file.file, file.filename)
        return f"https://{bucket_name}.s3.amazonaws.com/{file.filename}"
    except Exception as e:
        print("Something Happened: ", e)
        return False


def create_music(db: Session, music_order: schemas.MusicOrder, bucket_name: str, owner: artist_schemas.Artist) -> schemas.Music:
    uploaded_audio_file_url = upload_file_to_s3(
        music_order.audio_file, bucket_name)
    uploaded_cover_img_url = upload_file_to_s3(
        music_order.cover_file, bucket_name)
    db_music = models.Music(title=music_order.title, genre=music_order.genre._value_,
                            audio_file_url=uploaded_audio_file_url, cover_img_url=uploaded_cover_img_url, owner_id=owner.id)
    db.add(db_music)
    db.commit()
    db.refresh(db_music)
    return db_music
