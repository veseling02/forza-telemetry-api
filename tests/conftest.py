import pytest
from config import settings
from database import Base, get_db
from main import app
import models
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

assert settings.test_database_url and "test" in settings.test_database_url, "TEST_DATABASE_URL must point at a test database"

test_engine = create_engine(settings.test_database_url)

TestSessionLocal = sessionmaker(bind=test_engine)

def override_get_db():
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()
        
@pytest.fixture
def client():
    Base.metadata.create_all(test_engine)
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()
    Base.metadata.drop_all(test_engine)
    
@pytest.fixture
def auth_headers(client):
    client.post("/users", json={"username": "tester", "password": "test-password"})
    response = client.post("/token", data={"username": "tester", "password": "test-password"})
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}