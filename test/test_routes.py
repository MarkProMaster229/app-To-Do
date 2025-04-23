from inside import app
from unittest.mock import patch
import pytest

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@patch('inside.db')
def test_login_success(mock_db, client):
    mock_db.check_user.return_value = True

    response = client.post('/', data={
        'username': 'testuser',
        'password': 'secret',
        'action': 'login'
    }, follow_redirects=False)

    assert response.status_code == 302
    assert '/rol' in response.headers['Location']
