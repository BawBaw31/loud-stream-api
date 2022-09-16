from datetime import timedelta

from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sql_app.core.config import Settings
from sqlalchemy.orm import Session

from ..core.dependencies import get_current_user, get_db, get_settings
from . import schemas
from .crud import authenticate_user, create_access_token, create_user

router = APIRouter(
    prefix="",
    tags=["users"],
)


@router.post("/token", response_model=schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),
                                 db: Session = Depends(get_db), settings: Settings = Depends(get_settings)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(
        minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user.email}, secret=settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/register", response_model=schemas.User)
async def register_user(user: schemas.UserCreate = Body(title="user create"), db: Session = Depends(get_db)):
    return create_user(db, user)


@router.get("/me/", response_model=schemas.User)
async def read_users_me(current_user: schemas.User = Depends(get_current_user)):
    return current_user
