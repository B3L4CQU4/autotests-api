import httpx
BASE_URL = "http://localhost:8000"

login_payload = {
  "email": "user@example.com",
  "password": "string"
}
with httpx.Client() as client:
  try:
    login_response = client.post(f"{BASE_URL}/api/v1/authentication/login", json=login_payload)
    login_response.raise_for_status()
    access_token = login_response.json()["token"]["accessToken"]
    access_headers= {"Authorization": f"Bearer {access_token}"}
    about_response = client.get(f"{BASE_URL}/api/v1/users/me", headers=access_headers)
    login_response.raise_for_status()
    print(f"{about_response.json()} {about_response.status_code}")
  except httpx.HTTPStatusError as e:
    print(f"Ошибка запроса: {e}\nОтвет: {e.response.status_code} {e.response.text}")
  except KeyError as e:
    print(f"Ошибка: в ответе отсутствует ожидаемый ключ {e}")
  except Exception as e:
    print(f"Неожиданная ошибка: {e}")
  finally:
    client.close()


