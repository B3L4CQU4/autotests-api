import httpx
from tools.fakers import get_random_email
BASE_URL = "http://localhost:8000"

create_payload = {
    "email": get_random_email(),
    "password": "string",
    "lastName": "string",
    "firstName": "string",
    "middleName": "string"
}

try:
    """Создание пользователя"""
    create_response = httpx.post(f"{BASE_URL}/api/v1/users", json=create_payload)
    create_response.raise_for_status()
    print(f"{create_response.json()}\n{create_response.status_code}\n\n")

    """Создание пейлоада для авторизации"""
    email = create_response.json()["user"]["email"]
    login_payload = {
        "email": email,
        "password": "string",
    }

    """Авторизация"""
    login_response = httpx.post(f"{BASE_URL}/api/v1/authentication/login", json=login_payload)
    login_response.raise_for_status()
    print(f"{login_response.json()}\n{login_response.status_code}\n\n")

    """Подготовка заголовков для обновления"""
    access_token = login_response.json()["token"]["accessToken"] 
    headers = {
        "Authorization":f"Bearer {access_token}"
    }

    """Получение id пользователя"""
    user_id = create_response.json()["user"]["id"]

    """Создание пейлоада для обновления"""
    update_payload = {
        "email": get_random_email(),
        "lastName": "string",
        "firstName": "string",
        "middleName": "string"
    }

    """Обновление пользователя"""
    update_response = httpx.patch(f"{BASE_URL}/api/v1/users/{user_id}", json=update_payload, headers=headers)
    update_response.raise_for_status()
    print(f"{update_response.json()}\n{update_response.status_code}\n\n")

except httpx.HTTPStatusError as e:
    print(f"Ошибка запроса: {e}\nОтвет: {e.response.status_code} {e.response.text}")
except KeyError as e:
    print(f"Ошибка: в ответе отсутствует ожидаемый ключ {e}")
except Exception as e:
    print(f"Неожиданная ошибка: {e}")