import pytest
from fastapi import FastAPI, status
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app import routers
from app.main import app  
from  app.database import get_db
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


def test_create_supplier(client):
    payload = {"name": "Acme Corp", "email": "acme@example.com"}

    response = client.post("/suppliers/", json=payload)

    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert "id" in data
    assert data["name"] == payload["name"]


def test_read_all_suppliers(client):
    payload_1 = {"name": "Acme Corp", "email": "acme@example.com"}
    payload_2 = {"name": "Globex", "email": "globex@example.com"}
    client.post("/suppliers/", json=payload_1)
    client.post("/suppliers/", json=payload_2)

    response = client.get("/suppliers/")

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 2


def test_read_supplier_by_id(client):
    payload = {"name": "Acme Corp", "email": "acme@example.com"}
    created = client.post("/suppliers/", json=payload).json()
    supplier_id = created["id"]

    response = client.get(f"/suppliers/{supplier_id}")

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == supplier_id
    assert data["name"] == "Acme Corp"


def test_read_supplier_not_found(client):
    response = client.get("/suppliers/999")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Supplier with ID 999 not found"


def test_delete_supplier(client):
    payload = {"name": "Acme Corp", "email": "acme@example.com"}
    created = client.post("/suppliers/", json=payload).json()
    supplier_id = created["id"]

    response = client.delete(f"/suppliers/{supplier_id}")

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert response.content == b""

    get_response = client.get(f"/suppliers/{supplier_id}")
    assert get_response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_supplier_not_found(client):
    response = client.delete("/suppliers/999")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Supplier with ID 999 not found"
