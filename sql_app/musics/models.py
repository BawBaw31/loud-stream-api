
import datetime

from sqlalchemy import (Column, DateTime, Enum, ForeignKey, Integer, String,
                        Table)
from sqlalchemy.orm import relationship

from ..core.database import Base
from ..musics.schemas import GenresEnum

music_collaborators = Table("music_collaborators", Base.metadata,
                            Column("music_id", Integer,
                                   ForeignKey("musics.id")),
                            Column("collaborator_id", Integer, ForeignKey("artists.id")))


class Music(Base):
    __tablename__ = "musics"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    audio_file_name = Column(String, unique=True)
    cover_file_name = Column(String, unique=True)
    streams = Column(Integer, default=0)
    genre = Column(String, Enum(GenresEnum))
    created_date = Column(DateTime, default=datetime.datetime.utcnow)
    owner_id = Column(Integer, ForeignKey("artists.id"))
    album_id = Column(Integer, ForeignKey("albums.id"))

    owner = relationship("Artist", back_populates="musics")
    album = relationship("Album", back_populates="musics")

    collaborators = relationship(
        "Artist", secondary=music_collaborators, backref='collaborations')
