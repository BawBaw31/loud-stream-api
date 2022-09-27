from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sql_app.core.database import get_db
from sqlalchemy.orm import Session

from ..artists import crud
from ..artists.schemas import TokenData
from .config import Settings, get_settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_current_artist(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db),
                             settings: Settings = Depends(get_settings)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[
            settings.jwt_algorithm])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
    artist = crud.get_artist_by_email(db, email=token_data.email)
    if artist is None:
        raise credentials_exception
    return artist
