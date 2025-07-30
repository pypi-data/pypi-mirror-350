""" Модуль текстового сериализатора http клиента. """

import httpx

from rms_fastapi_service.clients.serializers.base import BaseSerializer


class HTTPXRawSerializer(BaseSerializer[httpx.Response, httpx.Response]):
    """ Класс текстового сериализатора. """
    @classmethod
    def serialize(cls, response: httpx.Response) -> httpx.Response:
        return response

    @classmethod
    def get_status_code(cls, response: httpx.Response) -> int:
        return response.status_code

    @classmethod
    def get_raw_text(cls, response: httpx.Response) -> str:
        return response.text
