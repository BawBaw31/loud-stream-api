
import datetime

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import relationship, validates

from ..core.database import Base


class Artist(Base):
    __tablename__ = "artists"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    stage_name = Column(String)
    hashed_password = Column(String)
    created_date = Column(DateTime, default=datetime.datetime.utcnow)

    musics = relationship("Music", back_populates="owner")
    albums = relationship("Album", back_populates="owner")

    @validates('email')
    def validate_email(self, key, address):
        if '@' not in address or '.' not in address:
            raise ValueError("failed simple email validation")
        return address

    @validates('stage_name')
    def validate_name(self, key, value):
        assert value != ''
        return value
