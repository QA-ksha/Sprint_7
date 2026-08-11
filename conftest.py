import pytest

import api
from helpers import generate_courier_data, get_login_payload


@pytest.fixture
def courier_payload():
    return generate_courier_data()


@pytest.fixture
def registered_courier():
    courier_data = generate_courier_data()

    api.create_courier(courier_data)

    yield courier_data

    login_response = api.login_courier(
        get_login_payload(courier_data)
    )
    courier_id = login_response.json().get("id")

    if courier_id:
        api.delete_courier(courier_id)

        