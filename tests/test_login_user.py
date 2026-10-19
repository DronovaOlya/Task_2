import requests
import allure
from urls import BASE_URL, LOGIN_USER
import pytest

@allure.epic('Авторизация пользователя')
class TestLoginUser:
    @allure.title('Успешная авторизация пользователя')
    def test_login_user(self, user_create, user_delete):
        payload = user_create
        response = requests.post(f"{BASE_URL}{LOGIN_USER}", json=payload)
        user_delete.update(payload)
                
        assert response.status_code == 200
        assert response.json()["success"] is True

    @pytest.mark.parametrize("payload",[
        {"email": "incorrect_test@yandex.ru", "title":"некорректным email"},                  
        {"password": "incorrect_password", "title":"некорректным password"},                     
        {"email": "incorrect_test@yandex.ru",
         "password": "incorrect_password", "title":"некорректным email и password"}, 
         {"email": "",
        "password": "incorrect_password", "title":"пустым email и некорректным password"},
        {"email": "incorrect_test@yandex.ru",
        "password": "", "title":"некорректным email и пустым password"},
        {"email": "",
        "password": "", "title":"пустым email и пустым password"},
    ])
    def test_login_user_incorrect_data(self, payload):
        allure.dynamic.title(f"Авторизация пользователя с {payload['title']}")
        response = requests.post(f"{BASE_URL}{LOGIN_USER}", json=payload)

        assert response.status_code == 401
        assert "message" in response.json() and "email or password are incorrect" in response.json()["message"]