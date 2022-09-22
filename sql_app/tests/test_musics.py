
import os
import pathlib

from fastapi import UploadFile
from fastapi.testclient import TestClient
from sql_app.core.storage import Storage
from sql_app.tests.test_artists import authenticate_util

from ..core.dependencies import get_db
from ..main import app
from .db_test_utils import override_get_db, test_db


class OverrideStorage:
    def upload_file_to_s3(self, file: UploadFile) -> str:
        return f"https://given-bucket.s3.amazonaws.com/{file.filename}"


app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[Storage] = OverrideStorage


client = TestClient(app)

audio_file_path = os.path.join(pathlib.Path(
    __file__).parent.absolute(), "fixtures", "given_audio_file.mp3")
cover_file_path = os.path.join(pathlib.Path(
    __file__).parent.absolute(), "fixtures", "given_cover_file.jpg")

given_files = {"audio_file": ("given_audio_file", open(audio_file_path, "rb"), "mp3"), "cover_file": (
    "given_cover_file", open(cover_file_path, "rb"), "image/jpeg")}
given_music = {"music_title": "test", "music_genre": "Pop"}


def musics_seed_util():
    token = authenticate_util(client)
    music = client.post(
        "/musics/", headers={"Authorization": f"Bearer {token}"}, data=given_music, files=given_files)
    return music.json()


def test_add_music(test_db):
    token = authenticate_util(client)
    response = client.post(
        "/musics/", headers={"Authorization": f"Bearer {token}"}, data=given_music, files=given_files)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == given_music["music_title"]
    assert data["genre"] == given_music["music_genre"]


def test_get_all_musics(test_db):
    music = musics_seed_util()
    response = client.get("/musics/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == music["title"]
    assert data[0]["genre"] == music["genre"]


def test_get_music_by_id(test_db):
    music = musics_seed_util()
    response = client.get(f"/musics/{music['id']}")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == music["title"]
    assert data["genre"] == music["genre"]


def test_get_music_by_title(test_db):
    music = musics_seed_util()
    response = client.get(f"/musics/?title={music['title']}")
    assert response.status_code == 200
    data = response.json()
    assert data[0]["title"] == music["title"]
    assert data[0]["genre"] == music["genre"]
