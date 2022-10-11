import datetime

from pydantic import BaseModel

from ..core.enums import GenresEnum


from ..artists.schemas import Artist


class AlbumBase(BaseModel):
    title: str
    cover_file_name: str
    genre: GenresEnum


class AlbumOrder(AlbumBase):
    pass


class Album(AlbumBase):
    id: int
    created_date: datetime.datetime
    owner: Artist
    published: bool

    class Config:
        orm_mode = True
