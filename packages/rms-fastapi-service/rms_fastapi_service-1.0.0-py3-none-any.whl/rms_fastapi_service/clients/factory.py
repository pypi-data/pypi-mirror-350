""" Модуль для работы с фабрикой клиента. """

from typing import (
    Generic,
    Type,
    TypeVar,
)

from rms_fastapi_service.clients.fast_api_client import FastAPIClient
from rms_fastapi_service.clients.serializers.base import BaseSerializer
from rms_fastapi_service.clients.transport.base_transport import BaseTransport


TInternal = TypeVar("TInternal")
TOutput = TypeVar("TOutput")


class FastAPIHTTPClientFactory(Generic[TInternal, TOutput]):
    """ Класс-фабрика для клиента. """
    @classmethod
    def build(
        cls,
        serializer: Type[BaseSerializer[TInternal, TOutput]],
        transport: Type[BaseTransport[TInternal]],
    ) -> Type[FastAPIClient[TInternal, TOutput]]:
        """
            Метод конструирования клиента в фабрике.

            Arguments:
                - serializer: Сериализатор для клиента;
                - transport: Транспорт для клиента.

            Returning:
                Ответ на незащищенный запрос.
        """
        class Client(FastAPIClient[TInternal, TOutput]):  # noqa: WPS431
            """ Класс клиента FastAPI. """
            SERIALIZER = serializer
            TRANSPORT = transport

        return Client
