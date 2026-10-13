from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health():
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

def test_create_session():
    response = client.post("/sessions", json=SESSION)
    
    assert response.status_code == 201
    assert response.json() == SESSION

def test_create_session_bad_sample():
    bad_sample = SESSION["samples"][0] | {"gas": 1.5}
    data = SESSION | {"samples": [bad_sample]}
    
    response = client.post("/sessions", json=data)
    
    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["body", "samples", 0, "gas"]