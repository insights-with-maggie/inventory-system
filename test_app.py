import pytest
from app import app

@pytest.fixture
def client():
    return app.test_client()

def test_get_inventory(client):
    response = client.get('/inventory')
    assert response.status_code == 200

def test_add_item(client):
    response = client.post('/inventory', json={
        "name": "Milk",
        "quantity": 5,
        "price": 10,
        "barcode": "737628064502"
    })
    assert response.status_code == 201

def test_update_item(client):
    client.post('/inventory', json={
        "name": "Milk",
        "quantity": 5,
        "price": 10,
        "barcode": "123"
    })

    response = client.patch('/inventory/1', json={"price": 20})
    assert response.status_code == 200

def test_delete_item(client):
    response = client.delete('/inventory/1')
    assert response.status_code == 200