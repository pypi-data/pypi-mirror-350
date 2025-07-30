""" Модуль сериализатора json для http клиента. """

import logging

import httpx
import orjson

from rms_fastapi_service.clients.schema.basic_types import Json
from rms_fastapi_service.clients.schema.exceptions import JsonSerializerDecodeError
from rms_fastapi_service.clients.serializers.base import BaseSerializer


logger = logging.getLogger(__name__)


class HTTPXOrjsonSerializer(BaseSerializer[httpx.Response, Json]):
    """ Класс http json сериализатора. """
    @classmethod
    def serialize(cls, response: httpx.Response) -> Json:
        try:
            return orjson.loads(response.text) if response.text else {}
        except orjson.JSONDecodeError as err:
            logger.error('[HTTPXOrjsonSerializer] Невозможно загрузить: %s', response.text)
            raise JsonSerializerDecodeError(msg=err.msg, doc=err.doc, pos=err.pos)

    @classmethod
    def get_status_code(cls, response: httpx.Response) -> int:
        return response.status_code

    @classmethod
    def get_raw_text(cls, response: httpx.Response) -> str:
        return response.text
