from fastapi.testclient import TestClient

from api.bill import responses
from run import app

client = TestClient(app)


def test_group_get():
    response = client.get('/group/get/0')
    print(response.status_code)
    print(response.json())


def test_group_by_type():
    response = client.get('/group/get/group')
    print(response.status_code)
    print(response.json())


def test_group_my():
    response = client.get('/group/my')
    print(response.status_code)
    print(response.json())


def test_group_create_equal():
    params = {
        "title": "string",
        "price": 0
    }

    register = client.post('/auth/register', json={'username': 'abcdefffffffffffffdfgadfg', 'password': 'qwerty1ihsdjfkh1123123'})
    print(register.json())

    login = client.post('/auth/login', json={'username': 'abcdefffffffffffffdfgadfg', 'password': 'qwerty1ihsdjfkh1123123'})
    token = login.json()["access_token"]
    print(login.json())

    response = client.post('/group/create_equal', headers={"Authorization": f"Bearer {token}"}, json=params)
    print(response.json())

