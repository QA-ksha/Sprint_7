import allure
import pytest

import api
from data import get_order_payload


class TestCreateOrder:

    @allure.title("Создание заказа с выбранным цветом")
    @pytest.mark.parametrize(
        "color",
        [
            ["BLACK"],
            ["GREY"],
            ["BLACK", "GREY"],
            None,
        ],
        ids=[
            "black",
            "grey",
            "black_and_grey",
            "without_color",
        ],
    )
    def test_can_create_order_with_different_colors(self, color):
        order_payload = get_order_payload(color=color)

        response = api.create_order(order_payload)

        assert response.status_code == 201
        assert response.json().get("track") is not None

        