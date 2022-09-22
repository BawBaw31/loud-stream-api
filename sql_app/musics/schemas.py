import datetime
import enum

from fastapi import UploadFile
from pydantic import BaseModel

from ..artists.schemas import Artist


class GenresEnum(enum.Enum):
    rock = "Rock"
    pop = "Pop"
    rap = "Rap"
    jazz = "Jazz"
    blues = "Blues"
    country = "Country"
    classical = "Classical"
    electronic = "Electronic"
    folk = "Folk"
    reggae = "Reggae"
    soul = "Soul"
    metal = "Metal"
    punk = "Punk"
    hip_hop = "Hip Hop"
    indie = "Indie"
    alternative = "Alternative"
    latin = "Latin"
    world = "World"
    dance = "Dance"
    rnb = "R&B"
    gospel = "Gospel"
    soundtrack = "Soundtrack"
    childrens = "Children's"
    comedy = "Comedy"
    spoken = "Spoken"
    holiday = "Holiday"
    new_age = "New Age"
    opera = "Opera"
    reggaeton = "Reggaeton"
    ska = "Ska"


class MusicBase(BaseModel):
    title: str
    genre: GenresEnum


class MusicOrder(MusicBase):
    audio_file: UploadFile
    cover_file: UploadFile


class Music(MusicBase):
    id: int
    streams: int
    audio_file_url: str
    cover_img_url: str
    created_date: datetime.datetime
    owner: Artist
    collaborators: list[Artist]

    class Config:
        orm_mode = True
