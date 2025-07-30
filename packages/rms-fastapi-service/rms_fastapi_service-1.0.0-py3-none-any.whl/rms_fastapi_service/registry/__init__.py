""" Модуль инициализации пакета регистри FastAPI. """

from rms_fastapi_service.registry.exception_handlers import DEFAULT_EXCEPTION_HANDLERS
from rms_fastapi_service.registry.log_config import DEFAULT_LOG_CONFIG
from rms_fastapi_service.registry.middlewares import DEFAULT_MIDDLEWARES


__all__ = (
    "DEFAULT_LOG_CONFIG",
    "DEFAULT_MIDDLEWARES",
    "DEFAULT_EXCEPTION_HANDLERS",
)
