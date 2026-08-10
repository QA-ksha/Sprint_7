import allure
import requests

from urls import (
    CREATE_COURIER_URL,
    DELETE_COURIER_URL,
    LOGIN_COURIER_URL,
    ORDERS_URL,
)


@allure.step("Создать курьера")
def create_courier(payload):
    return requests.post(CREATE_COURIER_URL, json=payload)


@allure.step("Авторизовать курьера")
def login_courier(payload):
    return requests.post(LOGIN_COURIER_URL, json=payload)


@allure.step("Удалить курьера")
def delete_courier(courier_id):
    return requests.delete(f"{DELETE_COURIER_URL}{courier_id}")


@allure.step("Создать заказ")
def create_order(payload):
    return requests.post(ORDERS_URL, json=payload)


@allure.step("Получить список заказов")
def get_orders():
    return requests.get(ORDERS_URL)

