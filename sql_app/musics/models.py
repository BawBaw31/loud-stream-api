
import datetime

from sql_app.musics.schemas import GenresEnum
from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from ..core.database import Base


class Music(Base):
    __tablename__ = "musics"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True, index=True)
    audio_file_url = Column(String, unique=True)
    cover_img_url = Column(String, unique=True)
    streams = Column(Integer, default=0)
    genre = Column(String, Enum(GenresEnum))
    created_date = Column(DateTime, default=datetime.datetime.utcnow)
    owner_id = Column(Integer, ForeignKey("artists.id"))
    # collaborator_id = Column(Integer, ForeignKey("artists.id"))

    owner = relationship("Artist", back_populates="musics")
    # collaborators = relationship("Artist", back_populates="collaborations")
