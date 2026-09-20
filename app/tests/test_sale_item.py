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


def test_create_sale_item(client):
    payload = {"sale_id": 10, "item_id": 5, "quantity": 2, "price": 15.99}

    response = client.post("/sale-items/", json=payload)

    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert "id" in data
    assert data["sale_id"] == payload["sale_id"]
    assert data["quantity"] == payload["quantity"]


def test_read_all_sale_items(client):
    payload_1 = {"sale_id": 10, "item_id": 5, "quantity": 2, "price": 15.99}
    payload_2 = {"sale_id": 11, "item_id": 6, "quantity": 1, "price": 9.99}
    client.post("/sale-items/", json=payload_1)
    client.post("/sale-items/", json=payload_2)

    response = client.get("/sale-items/")

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 2


def test_read_sale_item_by_id(client):
    payload = {"sale_id": 10, "item_id": 5, "quantity": 2, "price": 15.99}
    created = client.post("/sale-items/", json=payload).json()
    sale_item_id = created["id"]

    response = client.get(f"/sale-items/{sale_item_id}")

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == sale_item_id
    assert data["sale_id"] == 10


def test_read_sale_item_not_found(client):
    response = client.get("/sale-items/999")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Sale item with ID 999 not found"


def test_read_sale_items_by_sale(client):
    payload_1 = {"sale_id": 50, "item_id": 1, "quantity": 3, "price": 5.00}
    payload_2 = {"sale_id": 50, "item_id": 2, "quantity": 1, "price": 20.00}
    payload_3 = {"sale_id": 51, "item_id": 3, "quantity": 1, "price": 12.00}
    client.post("/sale-items/", json=payload_1)
    client.post("/sale-items/", json=payload_2)
    client.post("/sale-items/", json=payload_3)

    response = client.get("/sale-items/sale/50")

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 2
    assert all(item["sale_id"] == 50 for item in data)


def test_delete_sale_item(client):
    payload = {"sale_id": 10, "item_id": 5, "quantity": 2, "price": 15.99}
    created = client.post("/sale-items/", json=payload).json()
    sale_item_id = created["id"]

    response = client.delete(f"/sale-items/{sale_item_id}")

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert response.content == b""

    get_response = client.get(f"/sale-items/{sale_item_id}")
    assert get_response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_sale_item_not_found(client):
    response = client.delete("/sale-items/999")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Sale item with ID 999 not found"
