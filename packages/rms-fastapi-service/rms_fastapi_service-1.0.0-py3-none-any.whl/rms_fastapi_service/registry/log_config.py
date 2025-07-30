""" Модуль конфигурирования логирования в сервисе FastAPI. """

from rms_fastapi_service.logs.handlers import (
    LogFormat,
    LoggingConfig,
)


DEFAULT_LOG_CONFIG = LoggingConfig(
    level="INFO",
    formatting=LogFormat.JSON,
)
