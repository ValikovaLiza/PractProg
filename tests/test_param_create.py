import pytest
from helpers.api_client import APIClient
from helpers.schemas import CREATE_BOOKING_SCHEMA
from jsonschema import validate

# Валидные данные
valid_booking_data = [
    {
        "firstname": "A",
        "lastname": "B",
        "totalprice": 1,
        "depositpaid": False,
        "bookingdates": {
            "checkin": "2024-01-01",
            "checkout": "2024-01-02"
        }
    },
    {
        "firstname": "John",
        "lastname": "Doe",
        "totalprice": 500,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2024-11-01",
            "checkout": "2024-11-10"
        },
        "additionalneeds": "Breakfast"
    }
]

invalid_booking_data = [
    # Пропущенные обязательные поля
    (
        {
            ## а тут ошибка сервера
            "lastname": "Doe",
            "totalprice": 100,
            "depositpaid": True,
            "bookingdates": {
                "checkin": "2024-01-01",
                "checkout": "2024-01-10"
            }
        },
        500
    ),
    (
        {
            "firstname": "John", 
            "lastname": "Doe", 
            "totalprice": "abc", ## тут цена сама на null меняется
            "depositpaid": True, 
            "bookingdates": {
                "checkin": "2024-01-01", 
                "checkout": "2024-01-10"
            }
        }, 
    200
    )
]

@pytest.mark.parametrize("payload", valid_booking_data)
def test_create_booking_valid(payload):
    client = APIClient()
    response = client.create_booking(payload)
    assert response.status_code == 200

    validate(instance=response.json(), schema=CREATE_BOOKING_SCHEMA)

    booking_id = response.json()["bookingid"]
    token_response = client.get_token("admin", "password123")
    token = token_response.json()["token"]
    delete_response = client.delete_booking(booking_id, token)
    assert delete_response.status_code == 201


@pytest.mark.parametrize("payload, expected_status", invalid_booking_data)
def test_create_booking_invalid(payload, expected_status):
    client = APIClient()
    response = client.create_booking(payload)
    # print(f"Payload: {payload}")
    # print(f"Response: {response.status_code}, {response.text}")
    
    assert response.status_code == expected_status
