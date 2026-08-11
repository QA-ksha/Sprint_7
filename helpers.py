import random
import string


def generate_random_string(length):
    letters = string.ascii_lowercase
    return "".join(random.choice(letters) for _ in range(length))


def generate_courier_data(empty_field=None):
    courier_data = {
        "login": generate_random_string(10),
        "password": generate_random_string(10),
        "firstName": generate_random_string(10)
    }

    if empty_field is not None:
        courier_data[empty_field] = ""

    return courier_data


def get_login_payload(courier_data):
    return {
        "login": courier_data["login"],
        "password": courier_data["password"]
    }

