import pytest
from app.main import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index(client):
    response = client.get('/')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'running'

def test_ping_default(client):
    response = client.get('/ping')
    assert response.status_code == 200

def test_hash_endpoint(client):
    response = client.get('/hash?data=test')
    assert response.status_code == 200
    assert 'hash' in response.get_json()