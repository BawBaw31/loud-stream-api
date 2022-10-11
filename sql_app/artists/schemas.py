import datetime

from pydantic import BaseModel


class TokenData(BaseModel):
    email: str | None = None


class ArtistBase(BaseModel):
    email: str
    stage_name: str


class ArtistOrder(ArtistBase):
    password: str


class Artist(ArtistBase):
    id: int
    email: str
    created_date: datetime.datetime

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str
    user: ArtistBase
