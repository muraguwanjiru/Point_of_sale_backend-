from fastapi.testclient import TestClient
from  app.main import app

client = TestClient(app)    

def test_root():
    endpoint = "/"
    response = client.get(endpoint)
    print(response.json())
    print(response.status_code)
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the POS API!"}