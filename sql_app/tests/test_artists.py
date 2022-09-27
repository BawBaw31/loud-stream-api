
from fastapi.testclient import TestClient
from sql_app.core.database import get_db

from ..main import app
from .db_test_utils import override_get_db, test_db

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

given_user = {"email": "test@test.test",
              "stage_name": "test", "password": "test"}


def authenticate_util(client):
    client.post(
        "/register", headers={"Content-Type": "application/json"}, json=given_user)
    login = client.post("/token", headers={"Content-Type": "application/x-www-form-urlencoded"}, data={
        "username": given_user["email"], "password": given_user["password"]})
    return login.json().get("access_token")


def test_register_artist(test_db):
    response = client.post(
        "/register", headers={"Content-Type": "application/json"}, json=given_user)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@test.test"
    assert data["stage_name"] == "test"


def test_login_for_access_token(test_db):
    client.post(
        "/register", headers={"Content-Type": "application/json"}, json=given_user)
    response = client.post("/token", headers={"Content-Type": "application/x-www-form-urlencoded"}, data={
                           "username": given_user["email"], "password": given_user["password"]})
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "token_type" in data


def test_me(test_db):
    token = authenticate_util(client)
    response = client.get("/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == given_user["email"]
    assert data["stage_name"] == given_user["stage_name"]
