import pytest
import allure

import api
import data
from helpers import get_login_payload


class TestLoginCourier:

    @allure.title("Успешная авторизация курьера")
    def test_courier_can_log_in(self, registered_courier):
        login_payload = get_login_payload(registered_courier)

        response = api.login_courier(login_payload)

        assert response.status_code == 200
        assert response.json().get("id") is not None

    @allure.title("Авторизация с неверным логином")
    def test_courier_cannot_log_in_with_wrong_login(self, registered_courier):
        login_payload = get_login_payload(registered_courier)
        login_payload["login"] = "unknown_courier"

        response = api.login_courier(login_payload)

        assert response.status_code == 404
        assert response.json()["message"] == data.LOGIN_WRONG_CREDENTIALS_ERROR

    @allure.title("Авторизация с неверным паролем")
    def test_courier_cannot_log_in_with_wrong_password(self, registered_courier):
        login_payload = get_login_payload(registered_courier)
        login_payload["password"] = "wrong_password"

        response = api.login_courier(login_payload)

        assert response.status_code == 404
        assert response.json()["message"] == data.LOGIN_WRONG_CREDENTIALS_ERROR

    @allure.title("Авторизация без логина")
    def test_courier_cannot_log_in_without_login(self, registered_courier):
        login_payload = get_login_payload(registered_courier)
        del login_payload["login"]

        response = api.login_courier(login_payload)

        assert response.status_code == 400
        assert response.json()["message"] == data.LOGIN_MISSING_DATA_ERROR

    @pytest.mark.xfail(reason="BUG-001: API возвращает 504 вместо 400 без password")
    @allure.issue(
        "BUG-001",
        "Авторизация без пароля возвращает 504 вместо 400"
    )
    @allure.title("Авторизация без пароля")
    @allure.description(
        "Известный баг: при авторизации без поля password API возвращает "
        "504 Service unavailable вместо ожидаемого 400."
    )
    def test_courier_cannot_log_in_without_password(self, registered_courier):
        login_payload = get_login_payload(registered_courier)
        del login_payload["password"]

        response = api.login_courier(login_payload)

        assert response.status_code == 400
        assert response.json()["message"] == data.LOGIN_MISSING_DATA_ERROR

        