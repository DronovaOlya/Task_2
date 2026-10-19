import requests
import allure
from urls import BASE_URL, CREATE_ORDER

@allure.epic('Получение заказов пользователя')
class TestReceiveOrderUser:
    @allure.title('Получение заказов авторизованного пользователя')
    def test_receive_order_auth_user(self, user_create, user_authorization, user_delete):
        response = requests.get(f"{BASE_URL}{CREATE_ORDER}", headers={"Authorization": user_authorization})
        user_delete.update(user_create)

        assert response.status_code == 200
        assert response.json()["success"] is True
        assert "orders" in response.json()

    @allure.title('Получение заказов неавторизованного пользователя')
    def test_receive_order_unauthorized_user(self):
        response = requests.get(f"{BASE_URL}{CREATE_ORDER}")
        
        assert response.status_code == 401
        assert response.json()["success"] is False
        assert "message" in response.json() and "You should be authorised" in response.json()["message"]
        
  