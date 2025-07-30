""" Модуль для работы с проверками http. """

from rms_fastapi_service.clients.httpx import HttpxClient


class HttpxHealthCheck:
    """ Класс для работы с проверками http. """
    def __init__(self, name: str, client: HttpxClient, ping_url: str):
        self.NAME = name
        self._client = client
        self._url = ping_url

    async def is_health(self) -> bool:
        """
            Метод проверки стабильной работы.

            Returning:
                Флаг, определяющий стабильность работы.
        """
        try:
            status, _ = await self._client.ping(url=self._url)
            return status
        except BaseException:  # noqa: WPS424
            return False
