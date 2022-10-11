import datetime

from pydantic import BaseModel

from ..albums.schemas import Album
from ..artists.schemas import Artist
from ..core.enums import GenresEnum


class MusicBase(BaseModel):
    title: str
    genre: GenresEnum


class MusicOrder(MusicBase):
    audio_file_name: str
    cover_file_name: str


class Music(MusicOrder):
    id: int
    streams: int
    created_date: datetime.datetime
    owner: Artist
    collaborators: list[Artist]
    album: Album
    published: bool

    class Config:
        orm_mode = True
