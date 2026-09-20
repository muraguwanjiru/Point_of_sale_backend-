import pytest
from fastapi import FastAPI, status
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app import routers
from  app.main import app 
from  app.database import get_db
from  app.dependencies import get_current_user

# Setup isolated in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Use your actual SQLAlchemy Base model here to create tables
# from database import Base 
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


def test_create_receipt(client):
    payload = {"merchant": "Target", "amount": 45.99, "date": "2026-09-20"}

    response = client.post("/receipts/", json=payload)

    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert "id" in data
    assert data["merchant"] == payload["merchant"]
    assert data["amount"] == payload["amount"]


def test_read_all_receipts(client):
    payload_1 = {"merchant": "Target", "amount": 45.99, "date": "2026-09-20"}
    payload_2 = {"merchant": "Walmart", "amount": 12.50, "date": "2026-09-19"}
    client.post("/receipts/", json=payload_1)
    client.post("/receipts/", json=payload_2)

    response = client.get("/receipts/")

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 2
    assert data[0]["merchant"] == "Target"
    assert data[1]["merchant"] == "Walmart"


def test_read_receipt_by_id(client):
    payload = {"merchant": "Target", "amount": 45.99, "date": "2026-09-20"}
    created = client.post("/receipts/", json=payload).json()
    receipt_id = created["id"]

    response = client.get(f"/receipts/{receipt_id}")

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == receipt_id
    assert data["merchant"] == "Target"


def test_update_receipt(client):
    payload = {"merchant": "Target", "amount": 45.99, "date": "2026-09-20"}
    created = client.post("/receipts/", json=payload).json()
    receipt_id = created["id"]

    update_payload = {"merchant": "Target Updated", "amount": 50.00, "date": "2026-09-20"}
    response = client.put(f"/receipts/{receipt_id}", json=update_payload)

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["merchant"] == "Target Updated"
    assert data["amount"] == 50.00


def test_delete_receipt(client):
    payload = {"merchant": "Target", "amount": 45.99, "date": "2026-09-20"}
    created = client.post("/receipts/", json=payload).json()
    receipt_id = created["id"]

    response = client.delete(f"/receipts/{receipt_id}")
    assert response.status_code == status.HTTP_200_OK

    get_response = client.get(f"/receipts/{receipt_id}")
    assert get_response.status_code == status.HTTP_404_NOT_FOUND
