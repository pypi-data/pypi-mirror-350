""" Модуль транспортировки httpx. """

from typing import Optional

import httpx

from rms_fastapi_service.clients.schema.basic_types import (
    Headers,
    HTTPMethods,
    Json,
    Params,
    RequestFiles,
)
from rms_fastapi_service.clients.schema.config import HttpClientConf
from rms_fastapi_service.clients.schema.exceptions import (
    HTTPTimeoutError,
    HTTPTransportError,
)
from rms_fastapi_service.clients.transport.base_transport import BaseTransport


class HTTPXTransport(BaseTransport[httpx.Response]):
    """ Класс реализации транпортировки httpx. """
    def __init__(self, client: Optional[httpx.AsyncClient] = None) -> None:
        self._client: Optional[httpx.AsyncClient] = client

    async def startup(self, conf: HttpClientConf) -> None:
        if self._client is not None:
            raise RuntimeError("Клиент уже запущен")
        self._client = httpx.AsyncClient(
            timeout=httpx.Timeout(conf.timeout),
            limits=httpx.Limits(
                max_connections=conf.limit,
                max_keepalive_connections=max(conf.limit // 2, 1),
            ),
            **conf.client_kwargs,
        )

    async def shutdown(self, conf: HttpClientConf) -> None:
        if self._client is None:
            raise RuntimeError("Клиент не запущен")
        await self._client.aclose()
        self._client = None

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
    ) -> httpx.Response:
        if self._client is None:
            raise RuntimeError("Клиент не запущен")
        httpx_timeout: Optional[httpx.Timeout] = None
        if timeout is not None:
            httpx_timeout = httpx.Timeout(timeout)
        try:
            return await self._client.request(
                method=method,
                url=url,
                content=body,  # type: ignore
                headers=headers,
                params=params,
                timeout=httpx_timeout or httpx.USE_CLIENT_DEFAULT,
                files=files,  # type: ignore
            )
        except httpx.TimeoutException as exc:
            raise HTTPTimeoutError from exc
        except Exception as exc:
            raise HTTPTransportError from exc
