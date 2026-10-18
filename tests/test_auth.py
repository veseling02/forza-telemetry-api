from config import settings

USER = {"username": "tester", "password": "test-password"}

def test_create_user(client):
    response = client.post("/users", json=USER)
    body = response.json()
    
    assert response.status_code == 201
    assert body["username"] == "tester"
    assert "password" not in body
    assert "password_hash" not in body
    assert "id" in body    
    
def test_user_duplicate(client):
    client.post("/users", json=USER)
    response = client.post("/users", json=USER)
    
    assert response.status_code == 409
    assert response.json()["detail"] == "Username is already taken!"
    
def test_create_user_short_pass(client):
    short_password = USER | {"password": "short"}
    response = client.post("/users", json=short_password)
    
    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["body", "password"]
    
def test_login(client):
    client.post("/users", json=USER)
    response = client.post("/token", data=USER)
    
    assert response.status_code == 200
    assert response.json()["token_type"] == "bearer"
    assert "access_token" in response.json()
    
def test_login_wrong_pass(client):
    wrong_pass = USER | {"password": "wrong"}
    client.post("/users", json=USER)
    response = client.post("/token", data=wrong_pass)
    
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect username or password"
    
def test_login_unknown_user(client):
    response = client.post("/token", data=USER)
    
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect username or password"
    
def test_read_me(client, auth_headers):
    response = client.get("/users/me", headers=auth_headers)
    
    assert response.status_code == 200
    assert response.json()["username"] == "tester"
    
def test_read_me_no_token(client):
    response = client.get("/users/me")
    
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"
    
def test_read_me_bad_token(client):
    response = client.get("/users/me", headers={"Authorization": "Bearer not-a-real-token"})
    
    assert response.status_code == 401
    assert response.json()["detail"] == "Could not validate credentials"

def test_registration_disabled(client, monkeypatch):
    monkeypatch.setattr(settings, "allow_registration", False)
    response = client.post("/users", json=USER)
    
    assert response.status_code == 403
    assert response.json()["detail"] == "Registration is disabled"