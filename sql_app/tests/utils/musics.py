
from fastapi import UploadFile
from fastapi.testclient import TestClient

from .artists import authenticate_util


def seed_music(client: TestClient, given_user: dict[str, str],
               given_music: dict[str, str], given_files: dict[str, UploadFile]):
    token = authenticate_util(client, given_user)
    music = client.post(
        "/musics/", headers={"Authorization": f"Bearer {token}"}, data=given_music, files=given_files)
    return music.json()
