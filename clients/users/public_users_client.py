from typing import TypedDict
from httpx import Response

from clients.api_client import APIClient

class CreateUserRequestDict(TypedDict):
  email: str
  password: str
  lastName: str
  firstName: str
  middleName: str

class PublicUsersClient(APIClient):
    """
    Клиент для работы с /api/v1/users
    """
    def create_user_api(
          self,
          request: CreateUserRequestDict
        ) -> Response:
        """
        Метод выполняет создание пользователя.

        :param request: Словарь с email, password, фамилией, именем и отчеством.
        :return: Ответ от сервера в виде объекта httpx.Response
        """
        return self.post("/api/v1/users", json=request)
