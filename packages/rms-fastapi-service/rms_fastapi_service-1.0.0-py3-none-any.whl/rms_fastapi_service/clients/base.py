""" Модуль для работы с базовым клиентом HTTP. """

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
    PingResult,
    RequestFiles,
)


TResult = TypeVar("TResult")


class BaseHTTPClient(Generic[TResult], abc.ABC):
    """ Класс базового клиент http. """
    @abc.abstractmethod
    async def ping(
        self,
        url: str,
        method: HTTPMethods = HTTPMethods.GET,
        name: str = "ping",
        headers: Optional[Headers] = None,
        timeout: Optional[float] = None,
    ) -> PingResult:
        raise NotImplementedError("Вы должны переопределить метод ping")

    @abc.abstractmethod
    async def delete(
        self,
        url: str,
        name: str,
        params: Optional[Params] = None,
        headers: Optional[Headers] = None,
        timeout: Optional[float] = None,
        retry: int = 1,
    ) -> TResult:
        raise NotImplementedError("Вы должны переопределить метод delete")

    @abc.abstractmethod
    async def post(
        self,
        url: str,
        name: str,
        params: Optional[Params] = None,
        json: Optional[Json] = None,
        body: Optional[bytes] = None,
        headers: Optional[Headers] = None,
        timeout: Optional[float] = None,
        files: Optional[RequestFiles] = None,
        retry: int = 1,
    ) -> TResult:
        raise NotImplementedError("Вы должны переопределить метод post")

    @abc.abstractmethod
    async def put(
        self,
        url: str,
        name: str,
        params: Optional[Params] = None,
        json: Optional[Json] = None,
        body: Optional[bytes] = None,
        headers: Optional[Headers] = None,
        timeout: Optional[float] = None,
        retry: int = 1,
    ) -> TResult:
        raise NotImplementedError("Вы должны переопределить метод put")

    @abc.abstractmethod
    async def get(
        self,
        url: str,
        name: str,
        params: Optional[Params] = None,
        headers: Optional[Headers] = None,
        timeout: Optional[float] = None,
        retry: int = 1,
    ) -> TResult:
        raise NotImplementedError("Вы должны переопределить метод get")

    @abc.abstractmethod
    async def patch(  # noqa: WPS211
        self,
        url: str,
        name: str,
        json: Optional[Json] = None,
        body: Optional[bytes] = None,
        headers: Optional[Headers] = None,
        params: Optional[Params] = None,
        timeout: Optional[float] = None,
        files: Optional[RequestFiles] = None,
        retry: int = 1,
    ) -> TResult:
        raise NotImplementedError("Вы должны переопределить метод patch")

    @abc.abstractmethod
    async def request(  # noqa: WPS211
        self,
        method: HTTPMethods,
        url: str,
        name: str,
        json: Optional[Json] = None,
        body: Optional[bytes] = None,
        headers: Optional[Headers] = None,
        params: Optional[Params] = None,
        timeout: Optional[float] = None,
        files: Optional[RequestFiles] = None,
        retry: int = 1,
    ) -> TResult:
        raise NotImplementedError("Вы должны переопределить метод request")

    @abc.abstractmethod
    async def startup(self) -> None:
        raise NotImplementedError("Вы должны переопределить метод startup")

    @abc.abstractmethod
    async def shutdown(self) -> None:
        raise NotImplementedError("Вы должны переопределить метод shutdown")
