import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ...core.config import Settings, get_settings
from ...core.database import Base

settings: Settings = get_settings()

engine = create_engine(
    settings.database_url, connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


@pytest.fixture()
def test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)
