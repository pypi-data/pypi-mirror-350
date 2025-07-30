""" Базовый транспортный модуль для http клиента. """

import abc
from typing import (
    Generic,
    Optional,
    TypeVar,
)

from rms_fastapi_service.clients.schema.basic_types import (
    Headers,
    HTTPMethods,
    Json,
    Params,
    RequestFiles,
)
from rms_fastapi_service.clients.schema.config import HttpClientConf


TResponse = TypeVar("TResponse")


class BaseTransport(Generic[TResponse], abc.ABC):
    """ Класс, реализующий базовую транспортировку. """
    @abc.abstractmethod
    async def request(
        self,
        method: HTTPMethods,
        url: str,
        name: str,
        headers: Headers,
        json: Optional[Json] = None,
        body: Optional[bytes] = None,
        params: Optional[Params] = None,
        timeout: Optional[float] = None,
        files: Optional[RequestFiles] = None,
    ) -> TResponse:
        """
            Абстрактный метод выполенения запроса.

            Arguments:
                - method: Метод запроса;
                - url: Адрес запроса;
                - name: Название запроса;
                - headers: Заголовки запроса;
                - json: Данные запроса;
                - body: Тело запроса;
                - params: Параметры запроса;
                - timeout: Время ошидания ответа запроса;
                - files: Файлы в запросе.

            Returning:
                Ответ на запрос.
        """
        raise NotImplementedError()

    @abc.abstractmethod
    async def startup(self, conf: HttpClientConf) -> None:
        """
            Абстрактный метод запуска транспорта.

            Arguments:
                - conf: Конфигурация клиента.
        """
        raise NotImplementedError()

    @abc.abstractmethod
    async def shutdown(self, conf: HttpClientConf) -> None:
        """
            Абстрактный метод остановки транспорта.

            Arguments:
                - conf: Конфигурация клиента.
        """
        raise NotImplementedError()
