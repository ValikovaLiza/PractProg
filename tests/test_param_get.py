import pytest
from helpers.api_client import APIClient
from helpers.schemas import GET_TOKEN_SCHEMA
from jsonschema import validate

# Валидные данные
valid_token_data = [
    ("admin", "password123")
]

# Невалидные данные
invalid_token_data = [
    ("admin", ""),  # Пропущен пароль
    ("", "password123"),  # Пропущено имя пользователя
    ("invalid_user", "wrongpassword"),  # Неверные учетные данные
    ({}, 400) 
]

@pytest.mark.parametrize("username, password", valid_token_data)
def test_get_token_valid(username, password):
    client = APIClient()
    response = client.get_token(username, password)
    
    response_data = response.json()
    validate(instance=response_data, schema=GET_TOKEN_SCHEMA)
    assert response.status_code == 200


@pytest.mark.parametrize("username, password", invalid_token_data)
def test_get_token_invalid(username, password):
    client = APIClient()
    response = client.get_token(username, password)
    print(username, password, response)
    assert response.status_code == 400
