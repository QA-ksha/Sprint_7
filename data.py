CREATE_COURIER_DUPLICATE_LOGIN_ERROR = "Этот логин уже используется. Попробуйте другой."
CREATE_COURIER_MISSING_DATA_ERROR = "Недостаточно данных для создания учетной записи"
LOGIN_WRONG_CREDENTIALS_ERROR = "Учетная запись не найдена"
LOGIN_MISSING_DATA_ERROR = "Недостаточно данных для входа"


def get_order_payload(color=None):
    payload = {
        "firstName": "Иван",
        "lastName": "Петров",
        "address": "г. Москва, ул. Тестовая, 1",
        "metroStation": 4,
        "phone": "+7 900 123 45 67",
        "rentTime": 5,
        "deliveryDate": "2026-08-20",
        "comment": "Тестовый заказ"
    }

    if color is not None:
        payload["color"] = color

    return payload

