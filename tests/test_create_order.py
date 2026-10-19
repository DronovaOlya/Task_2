import requests
import allure
from urls import BASE_URL, CREATE_ORDER
import pytest
from data import INGREDIENTS_1, INGREDIENTS_2, INGREDIENTS_3 

@allure.epic('Создание заказов')
class TestCreateOrder:
    @pytest.mark.parametrize(
                "ingredients, status, success, title", [
                    (INGREDIENTS_1, 200 , True, "корректными данными"),
                    (INGREDIENTS_2, 500, False, "некорректными данными"),
                    (INGREDIENTS_3, 400, False, "пустыми данными")
                ])
    def test_create_auth_user(self, ingredients, status, success, title, user_create, user_authorization, user_delete):
        allure.dynamic.title(f"Создание заказа у авторизованного пользователя с {title}")
        response = requests.post(f"{BASE_URL}{CREATE_ORDER}", json={"ingredients": ingredients}, headers={"Authorization": user_authorization})
        user_delete.update(user_create)
                
        assert response.status_code == status
        if success:
            assert response.json()["success"] is success

    @pytest.mark.parametrize(
                "ingredients, status, success, title", [
                    (INGREDIENTS_1, 200 , True, "корректными данными"),
                    (INGREDIENTS_2, 500, False, "некорректными данными"),
                    (INGREDIENTS_3, 400, False, "пустыми данными")
                ])
    def test_create_unauthorized_user(self, ingredients, status, success, title):
        allure.dynamic.title(f"Создание заказа у неавторизованного пользователя с {title}")
        response = requests.post(f"{BASE_URL}{CREATE_ORDER}", json={"ingredients": ingredients})
                
        assert response.status_code == status
        if success:
            assert response.json()["success"] is success