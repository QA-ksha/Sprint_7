import allure

import api


class TestOrderList:

    @allure.title("Получение списка заказов")
    @allure.description(
        "Проверка, что ответ содержит список заказов."
    )
    def test_get_orders_returns_orders_list(self):
        response = api.get_orders()

        assert response.status_code == 200
        assert "orders" in response.json()
        assert isinstance(response.json()["orders"], list)

        