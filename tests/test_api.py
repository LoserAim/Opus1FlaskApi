from src import app
import pytest


def test_get_index_page():
    with app.test_client() as client:
        response = client.get('/')
        assert response.status_code == 200


def test_get_users():
    with app.test_client() as client:
        response = client.get('/api/users')
        json_data = response.get_json()
        assert json_data == [{'email': 'bobsburgers@melissa.tv', 'id': 2, 'name': 'Bobby'}, {'email': 'Clarissa@melissa.tv', 'id': 3, 'name': 'Clarissa'}, {'email': 'darbus@melissa.tv', 'id': 4, 'name': 'Dave'}]

@pytest.mark.parametrize("id", [1])
def test_get_user_id(id):
    with app.test_client() as client:
        response = client.get(f'/api/users/{id}')
        json_data = response.get_json()
        assert json_data['id'] == id