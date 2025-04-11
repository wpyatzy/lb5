from fastapi.testclient import TestClient
from ..src.main import app

client = TestClient(app)

# Существующие пользователи
users = [
    {
        'id': 1,
        'name': 'Ivan Ivanov',
        'email': 'i.i.ivanov@mail.com',
    },
    {
        'id': 2,
        'name': 'Petr Petrov',
        'email': 'p.p.petrov@mail.com',
    }
]

def test_get_existed_user():
    '''Получение существующего пользователя'''
    response = client.get("/api/v1/user", params={'email': users[0]['email']})
    assert response.status_code == 200
    assert response.json() == users[0]

def test_get_unexisted_user():
    '''Получение несуществующего пользователя'''
    response = client.get("/api/v1/user", params={'email': "nonexistent@mail.com"})
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}

def test_create_user_with_valid_email():
    '''Создание пользователя с уникальной почтой'''
    new_user = {
        'name': 'New User',
        'email': 'new.user@mail.com'
    }
    response = client.post("/api/v1/user", json=new_user)
    assert response.status_code == 201
    assert response.json()['email'] == new_user['email']
    assert 'id' in response.json()

def test_create_user_with_invalid_email():
    '''Создание пользователя с почтой, которую использует другой пользователь'''
    existing_email_user = {
        'name': 'Duplicate Email',
        'email': users[0]['email']
    }
    response = client.post("/api/v1/user", json=existing_email_user)
    assert response.status_code == 400
    assert response.json() == {"detail": "Email already registered"}

def test_delete_user():
    '''Удаление пользователя'''
    new_user = {
        'name': 'User to delete',
        'email': 'to.delete@mail.com'
    }
    create_response = client.post("/api/v1/user", json=new_user)
    user_id = create_response.json()['id']
    
    delete_response = client.delete(f"/api/v1/user/{user_id}")
    assert delete_response.status_code == 200
    assert delete_response.json() == {"message": "User deleted"}
    
    check_response = client.get("/api/v1/user", params={'email': new_user['email']})
    assert check_response.status_code == 404