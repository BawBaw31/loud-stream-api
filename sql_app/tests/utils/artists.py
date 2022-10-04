
def authenticate_util(client, given_artist):
    client.post(
        "/register", headers={"Content-Type": "application/json"}, json=given_artist)
    login = client.post("/token", headers={"Content-Type": "application/x-www-form-urlencoded"}, data={
        "username": given_artist["email"], "password": given_artist["password"]})
    return login.json().get("access_token")
