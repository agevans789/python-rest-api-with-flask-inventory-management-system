import pytest
from app import app, inventory

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_get_inventory(client):
    res = client.get('/inventory')
    assert res.status_code == 200
    assert len(res.get_json()) >= 2

def test_add_item(client):
    payload = {"name": "New Gadget", "quantity": 10}
    res = client.post('/inventory', json=payload)
    assert res.status_code == 201
    assert res.get_json()["name"] == "New Gadget"

def test_external_api_failure(client):
    # Testing a fake barcode
    res = client.get('/fetch-product/9999999999')
    assert res.status_code == 404
