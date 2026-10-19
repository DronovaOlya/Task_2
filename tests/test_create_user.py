import requests
import allure
from helpers import random_email
from urls import BASE_URL, CREATE_USER
import pytest
from data import password, name

@allure.epic("Создание пользователя")
class TestCreateUser:
    @allure.title('Успешное создание пользователя')
    def test_create_user(self, user_delete):
        email = random_email()
        payload = {"name": name,
                    "password": password,
                    "email": email}
        response = requests.post(f"{BASE_URL}{CREATE_USER}", json=payload)
        user_delete.update(payload)
        
        assert response.status_code == 200
        assert response.json()["success"] is True
        assert response.json()["user"]["email"] == email
        assert "accessToken" in response.json()

    @allure.title('Создание существующего пользователя') 
    def test_create_existing_user(self, user_create, user_delete):
        payload = user_create
        response = requests.post(f"{BASE_URL}{CREATE_USER}", json=payload)
        user_delete.update(payload)
        
        assert response.status_code == 403
        assert "message" in response.json() and "User already exists" in response.json()["message"]
        assert response.json()["success"] is False

    @pytest.mark.parametrize("payload",[ 
            {"password": "123456", "name": "Ivan","title":"без email"},
            {"email": random_email(), "name": "Ivan","title":"без password"},
            {"password": "123456", "email": random_email(),"title":"без name"}
        ]
        )
    def test_create_user_no_data(self, payload):
        allure.dynamic.title(f"Создание пользователя {payload['title']}")
        response = requests.post(f"{BASE_URL}{CREATE_USER}", json=payload)

        assert response.status_code == 403
        assert "message" in response.json() and "Email, password and name are required fields" in response.json()["message"]
        assert response.json()["success"] is False