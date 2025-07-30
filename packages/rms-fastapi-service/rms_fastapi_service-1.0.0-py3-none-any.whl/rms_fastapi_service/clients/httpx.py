""" Модуль работы с httpx клиентом. """

import asyncio
from logging import getLogger
from typing import (
    Optional,
    Type,
)

import httpx
import orjson
from httpx._types import RequestFiles  # noqa:WPS436
from typing_extensions import deprecated

from rms_fastapi_service.clients.fast_api_client import FastAPIClient
from rms_fastapi_service.clients.factory import FastAPIHTTPClientFactory
from rms_fastapi_service.clients.schema.basic_types import (
    Headers,
    Json,
    Params,
    PingResult,
)
from rms_fastapi_service.clients.schema.config import HttpClientConf
from rms_fastapi_service.clients.schema.constants import (
    BACKOFF,
    MAX_BACKOFF,
)
from rms_fastapi_service.clients.serializers.httpx_orjson_serializer import HTTPXOrjsonSerializer
from rms_fastapi_service.clients.serializers.httpx_raw_serializer import HTTPXRawSerializer
from rms_fastapi_service.clients.transport.httpx_trasport import HTTPXTransport
# from fast_api_service.metrics import MetricsCollector
from rms_fastapi_service.middlewares.correlation import get_correlation_id


logger = getLogger(__name__)


@deprecated("Use JsonHTTPXClient or RawHTTPXClient instead.")
class HttpxClient:  # noqa: WPS214
    """ Класс клиента httpx. """
    def __init__(self, name: str, conf: HttpClientConf) -> None:
        self._name = name
        self._base_url = conf.url
        self._limit = conf.limit
        self._timeout = conf.timeout
        self._bearer = conf.bearer
        self._backoff = conf.backoff
        self._headers = {"Authorization": f"Bearer {self._bearer}"} if conf.bearer else {}
        if conf.headers:
            self._headers.update(conf.headers)
        # self._metrics = MetricsCollector()
        self._session = self._create_session()

    async def shutdown(self) -> None:
        """ Метод остановки клиента. """
        await self._session.aclose()

    async def ping(
        self,
        url: str,
        headers: Optional[Headers] = None,
        timeout: Optional[float] = None,
    ) -> PingResult:
        """
            Метод проверки клиента методом пинг.

            Arguments:
                - url: Адрес запроса;
                - headers: Заголовки запроса;
                - timeout: Время ошидания ответа запроса.

            Returning:
                Результат ping запроса по адресу.
        """
        url = f"{self._base_url}{url}"
        logger.debug("--> [%s] PING: %s", self._name, url)
        headers = self._build_headers(headers=headers)

        try:
            resp = await self._session.get(
                url=url,
                headers=headers,
                timeout=httpx.Timeout(timeout or self._timeout),
            )
            logger.debug("<-- [%s] PING: %s %s", self._name, url, resp.status_code)
        except Exception as err:
            msg = f"{err.__class__.__name__} {err}"
            logger.exception("<-- [%s] PING: %s %s", self._name, url, msg)
            return False, msg

        if resp.status_code == httpx.codes.OK:
            return True, resp.text
        return False, f"{resp.status_code}: {resp.text}"

    async def delete(
        self,
        url: str,
        name: str,
        headers: Optional[Headers] = None,
        timeout: Optional[float] = None,
        retry: int = 1,
    ) -> Json:
        """
            Метод запроса удаления для клиента.

            Arguments:
                - url: Адрес запроса;
                - name: Название запроса;
                - headers: Заголовки запроса;
                - timeout: Время ошидания ответа запроса;
                - retry: Количество повторений в случае неудачи.

            Returning:
                Ответ на запрос удаления.
        """
        return await self._request(
            method="DELETE",
            url=url,
            name=name,
            headers=headers,
            timeout=timeout,
            retry=retry,
        )

    async def post(
        self,
        url: str,
        name: str,
        json: Optional[Json] = None,
        body: Optional[bytes] = None,
        headers: Optional[Headers] = None,
        timeout: Optional[float] = None,
        files: Optional[RequestFiles] = None,
        retry: int = 1,
    ) -> Json:
        """
            Метод запроса создания для клиента.

            Arguments:
                - url: Адрес запроса;
                - name: Название запроса;
                - json: Данные запроса;
                - body: Тело запрос;
                - headers: Заголовки запроса;
                - timeout: Время ошидания ответа запроса;
                - files: Файлы в запросе;
                - retry: Количество повторений в случае неудачи.

            Returning:
                Ответ на запрос создания.
        """
        return await self._request(
            method="POST",
            url=url,
            name=name,
            json=json,
            body=body,
            headers=headers,
            timeout=timeout,
            retry=retry,
            files=files,
        )

    async def put(
        self,
        url: str,
        name: str,
        json: Json,
        headers: Optional[Headers] = None,
        timeout: Optional[float] = None,
        files: Optional[RequestFiles] = None,
        retry: int = 1,
    ) -> Json:
        """
            Метод запроса изменения для клиента.

            Arguments:
                - url: Адрес запроса;
                - name: Название запроса;
                - json: Данные запроса;
                - headers: Заголовки запроса;
                - timeout: Время ошидания ответа запроса;
                - files: Файлы в запросе;
                - retry: Количество повторений в случае неудачи.

            Returning:
                Ответ на запрос изменения.
        """
        return await self._request(
            method="PUT",
            url=url,
            name=name,
            json=json,
            headers=headers,
            timeout=timeout,
            retry=retry,
            files=files,
        )

    async def get(
        self,
        url: str,
        name: str,
        params: Optional[Params] = None,
        headers: Optional[Headers] = None,
        timeout: Optional[float] = None,
        retry: int = 1,
    ) -> Json:
        """
            Метод запроса чтения для клиента.

            Arguments:
                - url: Адрес запроса;
                - name: Название запроса;
                - params: Параметры запроса;
                - headers: Заголовки запроса;
                - timeout: Время ошидания ответа запроса;
                - retry: Количество повторений в случае неудачи.

            Returning:
                Ответ на запрос чтения.
        """
        return await self._request(
            method="GET",
            url=url,
            name=name,
            params=params,
            headers=headers,
            timeout=timeout,
            retry=retry,
        )

    def _create_session(self) -> httpx.AsyncClient:
        """
            Метод создания сессии клиента.

            Returning:
                Асинхронный клиент с сессией.
        """
        return httpx.AsyncClient(
            timeout=httpx.Timeout(self._timeout),
            limits=httpx.Limits(
                max_connections=self._limit * 2,
                max_keepalive_connections=self._limit,
            ),
        )

    async def _unsafe_request(
        self,
        method: str,
        name: str,
        url: str,
        json: Optional[Json] = None,
        body: Optional[bytes] = None,
        params: Optional[Params] = None,
        headers: Optional[Headers] = None,
        timeout: Optional[float] = None,
        files: Optional[RequestFiles] = None,
    ) -> Json:
        """
            Внутренний метод выполенения незащищенного запроса.

            Arguments:
                - method: Метод запроса;
                - name: Название запроса;
                - url: Адрес запроса;
                - json: Данные запроса;
                - body: Тело запроса;
                - params: Параметры запроса;
                - headers: Заголовки запроса;
                - timeout: Время ошидания ответа запроса;
                - files: Файлы в запросе.

            Returning:
                Ответ на незащищенный запрос.
        """
        url = f"{self._base_url}{url}"
        body = orjson.dumps(json) if json else body
        logger.debug("--> [%s] %s: %s\n%s", self._name, method, url, body or "")

        headers = self._build_headers(headers=headers, json=json)
        # with self._metrics.client_hist(service=self._name, method=method, name=name):
        resp = await self._session.request(
            method=method,
            url=url,
            content=body,  # type: ignore
            params=params,
            files=files,  # type: ignore
            headers=headers,
            timeout=httpx.Timeout(timeout or self._timeout),
        )

        # self._metrics.client_counter(
        #     service=self._name,
        #     method=method,
        #     name=name,
        #     status=resp.status_code,
        # )
        logger.debug("<-- [%s] %s", self._name, resp.text)
        resp.raise_for_status()
        return orjson.loads(resp.text) if resp.text else {}

    async def _request(  # noqa:WPS211
        self,
        method: str,
        url: str,
        name: str,
        json: Optional[Json] = None,
        body: Optional[bytes] = None,
        params: Optional[Params] = None,
        headers: Optional[Headers] = None,
        timeout: Optional[float] = None,
        files: Optional[RequestFiles] = None,
        retry: int = 1,
    ) -> Json:
        """
            Внутренний метод выполенения запроса.

            Arguments:
                - method: Метод запроса;
                - url: Адрес запроса;
                - name: Название запроса;
                - json: Данные запроса;
                - body: Тело запроса;
                - params: Параметры запроса;
                - headers: Заголовки запроса;
                - timeout: Время ошидания ответа запроса;
                - files: Файлы в запросе;
                - retry: Количество повторений в случае неудачи.

            Returning:
                Ответ на незащищенный запрос.
        """
        backoff = self._backoff
        while retry > 0:
            retry -= 1
            try:
                return await self._unsafe_request(
                    method=method,
                    name=name,
                    url=url,
                    json=json,
                    body=body,
                    params=params,
                    headers=headers,
                    files=files,
                    timeout=timeout,
                )
            except httpx.RequestError as request_err:
                if retry == 0:
                    raise

                backoff *= BACKOFF
                backoff = MAX_BACKOFF if backoff > MAX_BACKOFF else backoff
                logger.warning("Ошибка запроса: %s", request_err)
                logger.warning("Сон: %.03fs", backoff)
                await asyncio.sleep(backoff)

        return {}

    def _build_headers(
        self,
        headers: Optional[Headers] = None,
        json: Optional[Json] = None,
    ) -> Headers:
        """
            Внутренний метод конструирования заголовков.

            Arguments:
                - headers: Заголовки запроса;
                - json: Данные запроса.

            Returning:
                Сконструированные заголовки запроса.
        """
        request_headers = headers or {}
        custom_headers = self._headers.copy()
        custom_headers.update(request_headers)
        if json is not None:
            custom_headers.update({"content-type": "application/json"})

        correlation_id = get_correlation_id()
        if correlation_id:
            custom_headers.update({"x-correlation-id": correlation_id})

        return custom_headers


RawHTTPXClient: Type[
    FastAPIClient[
        httpx.Response,
        httpx.Response,
    ]
] = FastAPIHTTPClientFactory[httpx.Response, httpx.Response].build(
    serializer=HTTPXRawSerializer,
    transport=HTTPXTransport,
)

JsonHTTPXClient: Type[FastAPIClient[httpx.Response, Json]] = FastAPIHTTPClientFactory[
    httpx.Response,
    Json,
].build(
    serializer=HTTPXOrjsonSerializer,
    transport=HTTPXTransport,
)
