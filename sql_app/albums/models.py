import datetime

from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from ..core.database import Base
from ..musics.schemas import GenresEnum


class Album(Base):
    __tablename__ = "albums"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    cover_file_name = Column(String, unique=True)
    genre = Column(String, Enum(GenresEnum))
    created_date = Column(DateTime, default=datetime.datetime.utcnow)
    owner_id = Column(Integer, ForeignKey("artists.id"))

    owner = relationship("Artist", back_populates="albums")
    musics = relationship("Music", back_populates="album")
