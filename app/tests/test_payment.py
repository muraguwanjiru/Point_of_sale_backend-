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


def test_create_payment(client):
    payload = {"amount": 250.00, "currency": "USD", "payment_method": "credit_card", "status": "pending"}

    response = client.post("/payments/", json=payload)

    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert "id" in data
    assert data["amount"] == payload["amount"]
    assert data["payment_method"] == payload["payment_method"]


def test_read_all_payments(client):
    payload_1 = {"amount": 250.00, "currency": "USD", "payment_method": "credit_card", "status": "pending"}
    payload_2 = {"amount": 15.50, "currency": "USD", "payment_method": "paypal", "status": "completed"}
    client.post("/payments/", json=payload_1)
    client.post("/payments/", json=payload_2)

    response = client.get("/payments/")

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 2


def test_read_payment_by_id(client):
    payload = {"amount": 250.00, "currency": "USD", "payment_method": "credit_card", "status": "pending"}
    created = client.post("/payments/", json=payload).json()
    payment_id = created["id"]

    response = client.get(f"/payments/{payment_id}")

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == payment_id
    assert data["amount"] == 250.00


def test_update_payment(client):
    payload = {"amount": 250.00, "currency": "USD", "payment_method": "credit_card", "status": "pending"}
    created = client.post("/payments/", json=payload).json()
    payment_id = created["id"]

    update_payload = {"amount": 250.00, "currency": "USD", "payment_method": "credit_card", "status": "completed"}
    response = client.put(f"/payments/{payment_id}", json=update_payload)

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["status"] == "completed"


def test_delete_payment(client):
    payload = {"amount": 250.00, "currency": "USD", "payment_method": "credit_card", "status": "pending"}
    created = client.post("/payments/", json=payload).json()
    payment_id = created["id"]

    response = client.delete(f"/payments/{payment_id}")
    assert response.status_code == status.HTTP_200_OK

    get_response = client.get(f"/payments/{payment_id}")
    assert get_response.status_code == status.HTTP_404_NOT_FOUND
