import datetime

from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None


class ArtistBase(BaseModel):
    email: str
    stage_name: str


class ArtistCreate(ArtistBase):
    password: str


class Artist(ArtistBase):
    id: int
    email: str
    created_date: datetime.datetime

    class Config:
        orm_mode = True
