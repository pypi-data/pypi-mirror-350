""" Модуль конфигурации логов. """

from logging import (
    Logger,
    getLogger,
)
from logging.config import dictConfig
from typing import (
    Any,
    Dict,
    Optional,
)

from rms_fastapi_service.logs.handlers import (
    LogFormat,
    LoggingConfig,
    handler_factory,
)
from rms_fastapi_service.logs.injectors import (
    inject_contextvars,
    inject_version,
)


class Logging:
    """ Класс для работы с логированием. """
    def __init__(
        self,
        app_name: str,
        app_level: str,
        log_format: LogFormat,
        loggers: Optional[Dict[str, str]] = None,
    ) -> None:
        self._app_name = app_name
        self._level = app_level

        self._formatters: Dict[str, Any] = {}
        self._handlers: Dict[str, Any] = {}
        self._loggers: Dict[str, Any] = {}
        self._root: Dict[str, Any] = {}

        self._setup_handler(log_format)
        self._setup_loggers(loggers)

    @property
    def config(self) -> Dict[str, Any]:
        """ Свойство получения конфига логирования. """
        return {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": self._formatters,
            "handlers": self._handlers,
            "loggers": self._loggers,
            "root": self._root,
        }

    def get_logger(self, name: Optional[str] = None) -> Logger:
        """
            Метод получения логгера.

            Arguments:
                - name: Название логгера.

            Returning:
                Полученный логгер.
        """
        return getLogger(name or self._app_name)

    def _setup_handler(self, log_format: LogFormat) -> None:
        """
            Метод настройки обработчика логирования.

            Arguments:
                - log_format: Формат логирования.
        """
        handler = handler_factory(log_format)
        self._formatters[handler.name] = handler.formatter
        self._handlers[handler.name] = handler.handler(self._level)
        self._loggers[self._app_name] = {"level": self._level}
        self._root = {"handlers": [handler.name], "level": self._level}

    def _setup_loggers(self, loggers: Optional[Dict[str, str]] = None) -> None:
        """
            Метод настройки и установки логгеров.

            Arguments:
                - loggers: Данные логгеров.
        """
        if not loggers:
            return

        for name, level in loggers.items():
            logger = self._loggers.get(name, {})
            logger["level"] = level
            self._loggers[name] = logger


def setup_logging(
    app_name: str,
    app_version: str,
    app_level: str,
    log_format: LogFormat,
    loggers: Optional[Dict[str, str]] = None,
) -> Logger:
    """
        Метод настройки логгирования.

        Arguments:
            - app_name: Название приложения;
            - app_version: Версия приложения;
            - app_level Уровень приложения;
            - log_format Формат логирования;
            - loggers Данные логгеров.

        Returning:
            Готовый логгер.
    """
    inject_version(version=app_version)
    inject_contextvars(fields={"correlation_id"})
    logconf = Logging(
        app_name=app_name,
        app_level=app_level,
        log_format=log_format,
        loggers=loggers,
    )
    dictConfig(logconf.config)
    return logconf.get_logger()


def init(config: LoggingConfig, name: str, version: str) -> Logger:
    """
        Метод инициализации модуля логирования.

        Arguments:
            - config: Конфигурация логирования;
            - name: Название приложения;
            - version: Версия приложения.
    """
    return setup_logging(
        app_name=name,
        app_version=version,
        app_level=config.level,
        loggers=config.loggers,
        log_format=config.formatting,
    )
