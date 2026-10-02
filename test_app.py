import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_login_page(client):
    response = client.get('/')
    assert response.status_code == 200

def test_login_success(client):
    response = client.post('/', data={'username': 'admin', 'password': 'admin123'}, follow_redirects=True)
    assert response.status_code == 200
    assert b'Bienvenue' in response.data

def test_login_fail(client):
    response = client.post('/', data={'username': 'admin', 'password': 'wrong'})
    assert b'Identifiants invalides' in response.data

def test_add_cours(client):
    client.post('/', data={'username': 'admin', 'password': 'admin123'})
    response = client.post('/dashboard', data={'matiere': 'Maths', 'jour': 'Lundi', 'heure': '08:00'}, follow_redirects=True)
    assert b'Maths' in response.data
