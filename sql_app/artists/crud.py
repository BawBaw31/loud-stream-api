from datetime import datetime, timedelta

from jose import jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from . import models, schemas

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password):
    return pwd_context.hash(password)


def get_artist(db: Session, artist_id: int):
    return db.query(models.Artist).filter(models.Artist.id == artist_id).first()


def get_artist_by_email(db: Session, email: str):
    return db.query(models.Artist).filter(models.Artist.email == email).first()


def get_artists(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Artist).offset(skip).limit(limit).all()


def create_artist(db: Session, artist: schemas.ArtistCreate):
    db_artist = models.Artist(email=artist.email, stage_name=artist.stage_name,
                              hashed_password=get_password_hash(artist.password))
    db.add(db_artist)
    db.commit()
    db.refresh(db_artist)
    return db_artist


# Authentication
def authenticate_artist(db: Session, email: str, password: str):
    artist = get_artist_by_email(db, email)
    if not artist:
        return False
    if not pwd_context.verify(password, artist.hashed_password):
        return False
    return artist


def create_access_token(data: dict, secret: str, algorithm: str, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, secret, algorithm=algorithm)
    return encoded_jwt
