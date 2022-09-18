
import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from ..core.database import Base


class Artist(Base):
    __tablename__ = "artists"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    stage_name = Column(String, unique=True)
    hashed_password = Column(String)
    created_date = Column(DateTime, default=datetime.datetime.utcnow)
    # collaboration_id = Column(Integer, ForeignKey("musics.id"))

    musics = relationship("Music", back_populates="owner")
    # collaborations = relationship("Music", back_populates="collaboration")
