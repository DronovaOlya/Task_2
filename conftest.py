import pytest
import requests
from urls import BASE_URL, LOGIN_USER, UPDATE_AND_DELETE_USER, CREATE_USER
from helpers import random_email
from data import password, name



@pytest.fixture
def user_delete():
    creds = {}
    yield creds
    login = requests.post(f"{BASE_URL}{LOGIN_USER}", json=creds)
    token = login.json()["accessToken"]
    requests.delete(f"{BASE_URL}{UPDATE_AND_DELETE_USER}", headers={"Authorization": token})

@pytest.fixture
def user_create():
    email = random_email()
    payload = {"name": name,
                "password": password,
                "email": email}
    requests.post(f"{BASE_URL}{CREATE_USER}", json=payload)
    return payload

@pytest.fixture
def user_authorization(user_create):
    payload = user_create
    response_login = requests.post(f"{BASE_URL}{LOGIN_USER}", json=payload)
    return response_login.json()["accessToken"]
