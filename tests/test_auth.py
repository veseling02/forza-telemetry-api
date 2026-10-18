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
    