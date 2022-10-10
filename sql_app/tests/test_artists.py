import pytest
from fastapi.testclient import TestClient

from ..core.database import get_db
from ..main import app
from .fixtures.artists import given_artist
from .utils.artists import authenticate_util
from .utils.db import override_get_db, test_db

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


@pytest.mark.usefixtures("test_db")
def test_register_artist():
    # When
    response = client.post(
        "/register", headers={"Content-Type": "application/json"}, json=given_artist)
    data = response.json()

    # Then
    assert response.status_code == 200
    assert data["email"] == given_artist["email"]
    assert data["stage_name"] == given_artist["stage_name"]


@pytest.mark.usefixtures("test_db")
def test_login_for_access_token():
    # When
    client.post(
        "/register", headers={"Content-Type": "application/json"}, json=given_artist)
    response = client.post("/token", headers={"Content-Type": "application/x-www-form-urlencoded"}, data={
                           "username": given_artist["email"], "password": given_artist["password"]})
    data = response.json()

    # Then
    assert response.status_code == 200
    assert "access_token" in data
    assert "token_type" in data


@pytest.mark.usefixtures("test_db")
def test_me():
    # When
    token = authenticate_util(client, given_artist)
    response = client.get("/me", headers={"Authorization": f"Bearer {token}"})

    # Then
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == given_artist["email"]
    assert data["stage_name"] == given_artist["stage_name"]
