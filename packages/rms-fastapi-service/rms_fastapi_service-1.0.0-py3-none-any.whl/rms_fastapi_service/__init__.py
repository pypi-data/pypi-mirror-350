""" Модуль инициализации пакета сервиса FastAPI. """

from rms_fastapi_service.clients import (
    HttpClientConf,
    HttpxClient,
    JsonHTTPXClient,
    RawHTTPXClient,
)
from rms_fastapi_service.exceptions import ServiceExceptionError
from rms_fastapi_service.factory import FastAPIFactory
from rms_fastapi_service.schemas import (
    BaseResponse,
    ErrorMessage,
    ErrorResponse,
    ServiceExceptionHandler,
    ServiceMiddleware,
)
from rms_fastapi_service.server import FastAPIServer
from rms_fastapi_service.utils import config_factory


__all__ = (
    "BaseResponse",
    "ErrorMessage",
    "ErrorResponse",
    "FastAPIServer",
    "FastAPIFactory",
    "HttpxClient",
    "HttpClientConf",
    "JsonHTTPXClient",
    "RawHTTPXClient",
    "ServiceExceptionError",
    "ServiceExceptionHandler",
    "ServiceMiddleware",
    "config_factory",
)
