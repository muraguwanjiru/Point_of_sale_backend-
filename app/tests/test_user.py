import pytest
from fastapi import FastAPI, status
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app import routers
from app import routers
from  app.main import app  
from app.database import get_db
from  app.dependencies import get_current_user

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

app = FastAPI()
app.include_router(routers)


@pytest.fixture(scope="function", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db_session():
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def client(db_session):
    app.dependency_overrides[get_db] = lambda: db_session
    app.dependency_overrides[get_current_user] = lambda: {"id": 1, "username": "testuser"}
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


def test_create_user(client):
    payload = {"username": "johndoe", "email": "john@example.com", "password": "securepassword"}

    response = client.post("/users/", json=payload)

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "id" in data
    assert data["username"] == payload["username"]
    assert data["email"] == payload["email"]


def test_read_all_users(client):
    payload_1 = {"username": "johndoe", "email": "john@example.com", "password": "securepassword"}
    payload_2 = {"username": "janedoe", "email": "jane@example.com", "password": "securepassword"}
    client.post("/users/", json=payload_1)
    client.post("/users/", json=payload_2)

    response = client.get("/users/")

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 2


def test_read_user_by_username(client):
    payload = {"username": "johndoe", "email": "john@example.com", "password": "securepassword"}
    client.post("/users/", json=payload)

    response = client.get("/users/username/johndoe")

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["username"] == "johndoe"


def test_read_user_by_id(client):
    payload = {"username": "johndoe", "email": "john@example.com", "password": "securepassword"}
    created = client.post("/users/", json=payload).json()
    user_id = created["id"]

    response = client.get(f"/users/{user_id}")

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == user_id
    assert data["username"] == "johndoe"


def test_update_user(client):
    payload = {"username": "johndoe", "email": "john@example.com", "password": "securepassword"}
    created = client.post("/users/", json=payload).json()
    user_id = created["id"]

    update_payload = {"username": "john_updated", "email": "john_new@example.com"}
    response = client.put(f"/users/{user_id}", json=update_payload)

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["username"] == "john_updated"
    assert data["email"] == "john_new@example.com"


def test_delete_user(client):
    payload = {"username": "johndoe", "email": "john@example.com", "password": "securepassword"}
    created = client.post("/users/", json=payload).json()
    user_id = created["id"]

    response = client.delete(f"/users/{user_id}")
    assert response.status_code == status.HTTP_200_OK

    get_response = client.get(f"/users/{user_id}")
    assert get_response.status_code == status.HTTP_404_NOT_FOUND
