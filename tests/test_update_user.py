import requests
import allure
from urls import BASE_URL, UPDATE_AND_DELETE_USER
import pytest
from helpers import random_email

@allure.epic('Изменения данных у пользователя')
class TestUpdateUser:
    @pytest.mark.parametrize("update_data",[
            {"email": random_email(),"title":"email"},                  
            {"password": "654321", "title":"password"},                     
            {"name": "Leon", "title":"name"}
        ])
    def test_update_user(self, user_create, user_authorization, update_data, user_delete):
        allure.dynamic.title(f"Изменение {update_data['title']} у авторизованного пользователя ")
        response = requests.patch(f"{BASE_URL}{UPDATE_AND_DELETE_USER}", json=update_data, headers={"Authorization": user_authorization})
        user_delete.update(user_create)
        if response.status_code == 200:
            user_delete.update(update_data)
        
        assert response.status_code == 200
        assert response.json()["success"] is True

    @pytest.mark.parametrize("update_data",[
            {"email": random_email(), "title":"email"},                  
            {"password": "654321", "title":"password"},                     
            {"name": "Leon", "title":"name"}
        ])
    def test_update_unauthorized_user(self, update_data):
        allure.dynamic.title(f"Изменение {update_data['title']} у неавторизованного пользователя ")
        response = requests.patch(f"{BASE_URL}{UPDATE_AND_DELETE_USER}", json=update_data)
        
        assert response.status_code == 401
        assert response.json()["success"] is False
        assert "message" in response.json() and "You should be authorised" in response.json()["message"]


