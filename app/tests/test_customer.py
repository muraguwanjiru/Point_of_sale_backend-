import pytest
from fastapi import FastAPI, status
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app import routers
from  app.main import app 
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


def test_create_customer(client):
    payload = {"name": "Alice Smith", "email": "alice@example.com", "phone": "1234567890"}

    response = client.post("/customers/", json=payload)

    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert "id" in data
    assert data["name"] == payload["name"]
    assert data["email"] == payload["email"]


def test_read_all_customers(client):
    payload_1 = {"name": "Alice Smith", "email": "alice@example.com", "phone": "1234567890"}
    payload_2 = {"name": "Bob Jones", "email": "bob@example.com", "phone": "0987654321"}
    client.post("/customers/", json=payload_1)
    client.post("/customers/", json=payload_2)

    response = client.get("/customers/")

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 2


def test_read_customer_by_id(client):
    payload = {"name": "Alice Smith", "email": "alice@example.com", "phone": "1234567890"}
    created = client.post("/customers/", json=payload).json()
    customer_id = created["id"]

    response = client.get(f"/customers/{customer_id}")

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == customer_id
    assert data["name"] == "Alice Smith"


def test_update_customer(client):
    payload = {"name": "Alice Smith", "email": "alice@example.com", "phone": "1234567890"}
    created = client.post("/customers/", json=payload).json()
    customer_id = created["id"]

    update_payload = {"name": "Alice Updated", "email": "alice_new@example.com"}
    response = client.put(f"/customers/{customer_id}", json=update_payload)

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["name"] == "Alice Updated"
    assert data["email"] == "alice_new@example.com"


def test_delete_customer(client):
    payload = {"name": "Alice Smith", "email": "alice@example.com", "phone": "1234567890"}
    created = client.post("/customers/", json=payload).json()
    customer_id = created["id"]

    response = client.delete(f"/customers/{customer_id}")
    assert response.status_code == status.HTTP_200_OK

    get_response = client.get(f"/customers/{customer_id}")
    assert get_response.status_code == status.HTTP_404_NOT_FOUND
