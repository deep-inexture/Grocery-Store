import json
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ..main import app
from ..database import Base, get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)


@pytest.fixture
def client():
    def override_get_db():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()
    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)
    yield client


@pytest.fixture
def token_header(client: TestClient):
    data = {
        "username": "testuser1@user1.in",
        "password": "TestUser@1234"
    }
    response = client.post("/login", json.dumps(data))
    access_token = response.json()["access_token"]
    return {"Authorization": f"Bearer {access_token}"}


@pytest.fixture
def admin_token_header(client: TestClient):
    data = {
        "username": "admin@admin.in",
        "password": "Admin@1234"
    }
    response = client.post("/login", json.dumps(data))
    access_token = response.json()["access_token"]
    return {"Authorization": f"Bearer {access_token}"}
