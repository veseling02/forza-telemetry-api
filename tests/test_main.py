def test_health(client):
    response = client.get("/health")
    
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
    
SESSION = {
    "started_at": "2026-09-25T21:14:00Z",
    "max_rpm": 8000.0,
    "samples": [
        {"t_ms": 0,
         "gas": 0.82,
         "brake": 0.0,
         "steer": -0.12,
         "speed_kmh": 143.6,
         "rpm": 6120.4},
    ],
}

def test_create_session(client, auth_headers):
    response = client.post("/sessions", json=SESSION, headers=auth_headers)
    
    assert response.status_code == 201
    assert "id" in response.json()
    assert "samples" not in response.json()
    assert response.json()["max_rpm"] == SESSION["max_rpm"]

def test_create_session_bad_sample(client, auth_headers):
    bad_sample = SESSION["samples"][0] | {"gas": 1.5}
    data = SESSION | {"samples": [bad_sample]}
    
    response = client.post("/sessions", json=data, headers=auth_headers)
    
    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["body", "samples", 0, "gas"]
    
def test_read_session(client, auth_headers):
    created = client.post("/sessions", json=SESSION, headers=auth_headers).json()
    session_id = created["id"]
    
    response = client.get(f"/sessions/{session_id}", headers=auth_headers)
    
    assert response.status_code == 200
    assert response.json()["samples"] == SESSION["samples"]
    
def test_read_missing_session(client, auth_headers):
    session_id = 999
    
    response = client.get(f"/sessions/{session_id}", headers=auth_headers)
    
    assert response.status_code == 404
    assert response.json() == {"detail": "Session not found"}
    
def test_read_session_bad_id(client, auth_headers):
    session_id = "abc"
    
    response = client.get(f"/sessions/{session_id}", headers=auth_headers)
    
    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["path", "session_id"]
    
def test_create_session_no_token(client):
    response = client.post("/sessions", json=SESSION)
    
    assert response.status_code == 401
    
def test_read_other_user_sessions(client, auth_headers):
    created = client.post("/sessions", json=SESSION, headers=auth_headers).json()
    session_id = created["id"]
    second_user_data = {"username": "other", "password": "other-password"}
    client.post("/users", json=second_user_data)
    login = client.post("/token", data=second_user_data)
    second_headers = {"Authorization": f"Bearer {login.json()['access_token']}"}
    
    response = client.get(f"/sessions/{session_id}", headers=second_headers)
    
    assert response.status_code == 404
    assert response.json() == {"detail": "Session not found"}