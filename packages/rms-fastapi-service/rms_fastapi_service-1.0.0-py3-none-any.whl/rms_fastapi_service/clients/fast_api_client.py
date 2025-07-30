""" Модуль определения клиента FastAPI. """

import asyncio
from logging import (
    DEBUG,
    getLogger,
)
from typing import (
    Generic,
    Optional,
    Type,
    TypeVar,
)

import orjson

from rms_fastapi_service.clients.base import BaseHTTPClient
from rms_fastapi_service.clients.schema.basic_types import (
    Headers,
    HTTPMethods,
    Json,
    Params,
    PingResult,
    RequestFiles,
)
from rms_fastapi_service.clients.schema.config import HttpClientConf
from rms_fastapi_service.clients.schema.constants import (
    BACKOFF,
    HTTP_HIGH_SUCCESS_CODE,
    HTTP_LOW_SUCCESS_CODE,
    HTTP_SUCCESS_CODE,
    MAX_BACKOFF,
)
from rms_fastapi_service.clients.schema.exceptions import (
    HTTPStatusCodeError,
    HTTPTransportError,
)
from rms_fastapi_service.clients.serializers.base import BaseSerializer
from rms_fastapi_service.clients.transport.base_transport import BaseTransport
# from fast_api_service.metrics import MetricsCollector
from rms_fastapi_service.middlewares.correlation import get_correlation_id


TInternal = TypeVar("TInternal")
TOutput = TypeVar("TOutput")

logger = getLogger(__name__)


def _is_request_success(status_code: int) -> bool:
    return HTTP_LOW_SUCCESS_CODE <= status_code <= HTTP_HIGH_SUCCESS_CODE


class FastAPIClient(Generic[TInternal, TOutput], BaseHTTPClient[TOutput]):  # noqa: WPS214
    SERIALIZER: Type[BaseSerializer[TInternal, TOutput]]
    TRANSPORT: Type[BaseTransport[TInternal]]

    def __init__(
        self,
        name: str,
        conf: HttpClientConf,
        # metrics_collector: Optional[MetricsCollector] = None,
    ) -> None:
        self._serializer = self.SERIALIZER()
        self._transport = self.TRANSPORT()
        self._client_name = name
        self._conf = conf
        # self._metrics_collector = metrics_collector or MetricsCollector()
        self._headers = {"Authorization": f"Bearer {conf.bearer}"} if conf.bearer else {}
        self._ignore_status = conf.ignore_status
        if conf.headers:
            self._headers.update(conf.headers)
        self._backoff = conf.backoff

    async def startup(self) -> None:
        await self._transport.startup(self._conf)

    async def shutdown(self) -> None:
        await self._transport.shutdown(self._conf)

    async def ping(
        self,
        url: str,
        method: HTTPMethods = HTTPMethods.GET,
        name: str = "ping",
        headers: Optional[Headers] = None,
        timeout: Optional[float] = None,
    ) -> PingResult:
        try:
            response = await self._request(
                method=method,
                url=url,
                name=name,
                headers=headers,
                timeout=timeout,
                retry=1,
            )
        except Exception as err:
            msg = f"{err.__class__.__name__} {err}"
            logger.exception("<-- [%s] PING: %s %s", self._client_name, url, msg)
            return False, msg
        return await self._build_ping_result(response)

    async def delete(
        self,
        url: str,
        name: str,
        params: Optional[Params] = None,
        headers: Optional[Headers] = None,
        timeout: Optional[float] = None,
        retry: int = 1,
    ) -> TOutput:
        return await self.request(
            method=HTTPMethods.DELETE,
            url=url,
            name=name,
            params=params,
            headers=headers,
            timeout=timeout,
            retry=retry,
        )

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
    ) -> TOutput:
        return await self.request(
            method=HTTPMethods.POST,
            url=url,
            name=name,
            json=json,
            body=body,
            params=params,
            files=files,
            headers=headers,
            timeout=timeout,
            retry=retry,
        )

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
    ) -> TOutput:
        return await self.request(
            method=HTTPMethods.PUT,
            url=url,
            name=name,
            params=params,
            json=json,
            body=body,
            headers=headers,
            timeout=timeout,
            retry=retry,
        )

    async def get(
        self,
        url: str,
        name: str,
        params: Optional[Params] = None,
        headers: Optional[Headers] = None,
        timeout: Optional[float] = None,
        retry: int = 1,
    ) -> TOutput:
        return await self.request(
            method=HTTPMethods.GET,
            url=url,
            name=name,
            params=params,
            headers=headers,
            timeout=timeout,
            retry=retry,
        )

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
    ) -> TOutput:
        return await self.request(
            method=HTTPMethods.PATCH,
            url=url,
            name=name,
            params=params,
            json=json,
            body=body,
            headers=headers,
            timeout=timeout,
            retry=retry,
        )

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
    ) -> TOutput:
        response = await self._request(
            method=method,
            url=url,
            name=name,
            json=json,
            body=body,
            headers=headers,
            params=params,
            timeout=timeout,
            files=files,
            retry=retry,
        )
        return self._serializer.serialize(response)

    async def _request(  # noqa: WPS211, WPS231
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
    ) -> TInternal:
        backoff = self._backoff
        url = f"{self._conf.url}{url}"
        body = orjson.dumps(json) if json else body
        headers = self._build_headers(headers=headers, json=json)
        while retry > 0:
            retry -= 1
            try:
                return await self._process_request(
                    method=method,
                    url=url,
                    name=name,
                    body=body,
                    headers=headers,
                    params=params,
                    timeout=timeout,
                    files=files,
                )
            except HTTPTransportError as exc:
                if retry == 0:
                    raise
                backoff *= BACKOFF
                backoff = MAX_BACKOFF if backoff > MAX_BACKOFF else backoff
                logger.warning("Ошибка запроса: %s", exc)
                logger.warning("Сон: %.03fs", backoff)
                await asyncio.sleep(backoff)
        raise RuntimeError("Недостижимый код")

    def _build_headers(
        self,
        headers: Optional[Headers] = None,
        json: Optional[Json] = None,
    ) -> Headers:
        request_headers = headers or {}
        custom_headers = self._headers.copy()
        custom_headers.update(request_headers)
        if json is not None:
            custom_headers.update({"content-type": "application/json"})

        correlation_id = get_correlation_id()
        if correlation_id:
            custom_headers.update({"x-correlation-id": correlation_id})

        return custom_headers

    async def _process_request(
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
    ) -> TInternal:
        logger.debug("--> [%s] %s: %s\n%s", self._client_name, method, url, body or "")
        # with self._metrics_collector.client_hist(
        #     service=self._client_name,
        #     method=method,
        #     name=name,
        # ):
        resp = await self._transport.request(
            method=method,
            url=url,
            name=name,
            json=json,
            body=body,
            headers=headers,
            params=params,
            timeout=timeout,
            files=files,
        )
        status_code = self._serializer.get_status_code(resp)
        # self._metrics_collector.client_counter(
        #     service=self._client_name,
        #     method=method,
        #     name=name,
        #     status=status_code,
        # )
        if logger.level == DEBUG:
            raw_text = self._serializer.get_raw_text(resp)
            logger.debug("<-- [%s] %d: %s", self._client_name, status_code, raw_text)
        if not self._ignore_status:
            self._validate_status(status_code)
        return resp

    async def _build_ping_result(self, response: TInternal) -> PingResult:
        """ Сборка результатов ping """
        status_code = self._serializer.get_status_code(response)
        text = self._serializer.get_raw_text(response)
        return status_code == HTTP_SUCCESS_CODE, f"{status_code}: {text}"

    def _validate_status(self, status_code: int) -> None:
        """ Валидация кода статуса, если требуется """
        if not _is_request_success(status_code):
            raise HTTPStatusCodeError(f"Invalid status code: {status_code}")
