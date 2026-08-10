from pathlib import Path

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

        if response.status_code == 504:
            screenshot_path = (
                Path(__file__).resolve().parent.parent
                / "screenshots"
                / "bug-001-login-without-password.jpg"
            )

            allure.attach.file(
                screenshot_path,
                name="BUG-001: API вернул 504 Service unavailable",
                attachment_type=allure.attachment_type.JPG,
            )

            allure.attach(
                response.text,
                name="Фактический ответ API",
                attachment_type=allure.attachment_type.TEXT,
            )

        assert response.status_code == 400
        assert response.json()["message"] == data.LOGIN_MISSING_DATA_ERROR

        