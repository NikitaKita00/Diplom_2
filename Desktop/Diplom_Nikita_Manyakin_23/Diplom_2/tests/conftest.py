import pytest
import requests
from utils.helpers import generate_random_email, generate_random_name
from utils.urls import URL_AUTH_REGISTER, URL_AUTH_USER, URL_INGREDIENTS


@pytest.fixture
def create_user():
    payload = {
        "email": generate_random_email(),
        "password": "password123",
        "name": generate_random_name(),
    }
    resp = requests.post(URL_AUTH_REGISTER, json=payload)
    resp.raise_for_status() 

    access_token = resp.json().get("accessToken", "").replace("Bearer ", "")
    payload["access_token"] = access_token

    try:
        yield payload
    finally:
        if access_token:
            try:
                requests.delete(
                    URL_AUTH_USER,
                    headers={"Authorization": f"Bearer {access_token}"},
                    timeout=10,
                )
            except requests.RequestException:
                pass


@pytest.fixture
def get_ingredients():
    resp = requests.get(URL_INGREDIENTS, timeout=10)
    resp.raise_for_status() 
    data = resp.json().get("data", [])
    return data