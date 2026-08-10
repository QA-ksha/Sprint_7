import allure
import pytest

import api
import data
from helpers import generate_courier_data


class TestCreateCourier:

    @allure.title("Создание курьера")
    def test_can_create_courier(self, courier_payload):
        response = api.create_courier(courier_payload)

        assert response.status_code == 201
        assert response.json() == {"ok": True}

    @allure.title("Нельзя создать двух одинаковых курьеров")
    def test_cannot_create_duplicate_courier(self, courier_payload):
        first_response = api.create_courier(courier_payload)
        assert first_response.status_code == 201

        second_response = api.create_courier(courier_payload)
        assert second_response.status_code == 409
        assert second_response.json()["message"] == data.CREATE_COURIER_DUPLICATE_LOGIN_ERROR

    @pytest.mark.parametrize("empty_field", ["login", "password"])
    @allure.title("Создание курьера без обязательного поля")
    def test_create_courier_missing_field(self, empty_field):
        courier_data = generate_courier_data(empty_field=empty_field)
        response = api.create_courier(courier_data)

        assert response.status_code == 400
        assert response.json()["message"] == data.CREATE_COURIER_MISSING_DATA_ERROR

    @allure.title("Нельзя создать курьера с занятым логином")
    def test_create_courier_existing_login(self, courier_payload):
        first_response = api.create_courier(courier_payload)
        assert first_response.status_code == 201

        duplicate_login_data = generate_courier_data()
        duplicate_login_data["login"] = courier_payload["login"]

        response = api.create_courier(duplicate_login_data)

        assert response.status_code == 409
        assert response.json()["message"] == data.CREATE_COURIER_DUPLICATE_LOGIN_ERROR

        