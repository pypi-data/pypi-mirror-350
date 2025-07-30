""" Модуль инициализации пакета схем FastAPI. """

from rms_fastapi_service.schemas.exception_handlers import ServiceExceptionHandler
from rms_fastapi_service.schemas.middlewares import ServiceMiddleware
from rms_fastapi_service.schemas.response import (
    BaseResponse,
    ErrorMessage,
    ErrorResponse,
)


__all__ = (
    "BaseResponse",
    "ErrorMessage",
    "ErrorResponse",
    "ServiceExceptionHandler",
    "ServiceMiddleware",
)
