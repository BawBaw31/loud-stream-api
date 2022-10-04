import pytest
from fastapi.testclient import TestClient

from ..core.database import get_db
from ..core.storage import Storage
from ..main import app
from .fixtures.artists import given_artist
from .fixtures.musics import given_files, given_music, given_wrong_files
from .utils.artists import authenticate_util
# test_db is used to override the get_db dependency
from .utils.db import override_get_db, test_db
from .utils.musics import seed_music
from .utils.storage import OverrideStorage

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[Storage] = OverrideStorage

client = TestClient(app)


@pytest.mark.usefixtures("test_db")
def test_add_music():
    # When
    token = authenticate_util(client, given_artist)
    response = client.post(
        "/musics/", headers={"Authorization": f"Bearer {token}"}, data=given_music, files=given_files)
    data = response.json()

    # Then
    assert response.status_code == 200
    assert data["title"] == given_music["music_title"]
    assert data["genre"] == given_music["music_genre"]
    assert given_music["music_title"].replace(
        " ", "_") in data["audio_file_name"]
    assert given_music["music_title"].replace(
        " ", "_") in data["cover_file_name"]


@pytest.mark.usefixtures("test_db")
def test_add_music_with_wrong_files_types():
    # When
    token = authenticate_util(client, given_artist)
    response = client.post(
        "/musics/", headers={"Authorization": f"Bearer {token}"}, data=given_music, files=given_wrong_files)
    data = response.json()

    # Then
    assert response.status_code == 400
    assert data["detail"]["audio_file"] == "Audio file must be mp3 or wav"
    assert data["detail"]["cover_file"] == "Cover file must be jpeg or png"


@pytest.mark.usefixtures("test_db")
def test_get_all_musics():
    # When
    music = seed_music(client, given_artist, given_music, given_files)
    response = client.get("/musics/")
    data = response.json()

    # Then
    assert response.status_code == 200
    assert len(data) == 1
    assert data[0]["title"] == music["title"]
    assert data[0]["genre"] == music["genre"]


@pytest.mark.usefixtures("test_db")
def test_stream_music_by_id():
    # When
    music = seed_music(client, given_artist, given_music, given_files)
    response = client.get(f"/musics/{music['id']}")

    # Then
    assert response.status_code == 200
    assert response.headers["content-type"] in ["audio/mpeg", "audio/wav"]
