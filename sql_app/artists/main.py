from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sql_app.core.config import Settings
from sql_app.core.database import get_settings
from sqlalchemy.orm import Session

from ..core.dependencies import get_current_artist, get_db
from . import schemas
from .crud import authenticate_artist, create_access_token, create_artist

router = APIRouter(
    prefix="",
    tags=["artists"],
)


@router.post("/token", response_model=schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),
                                 db: Session = Depends(get_db), settings: Settings = Depends(get_settings)):
    artist = authenticate_artist(db, form_data.username, form_data.password)
    if not artist:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(
        minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": artist.email}, secret=settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/register", response_model=schemas.Artist)
async def register_artist(artist: schemas.ArtistCreate, db: Session = Depends(get_db)):
    return create_artist(db, artist)


@router.get("/me/", response_model=schemas.Artist)
async def get_current_artist(current_artist: schemas.Artist = Depends(get_current_artist)):
    return current_artist
