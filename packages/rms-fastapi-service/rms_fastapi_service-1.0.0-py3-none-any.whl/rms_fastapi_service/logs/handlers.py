""" Модуль реализующих обработчики логирования. """

from dataclasses import (
    dataclass,
    field,
)
from enum import Enum
from typing import (
    Any,
    Dict,
)


class LogFormat(Enum):
    """ Описание всех типов форматов логов. """
    CONSOLE = "console"
    JSON = "json"


@dataclass
class LoggingConfig:
    """ Класс данных конфигурации логирования. """
    level: str
    formatting: LogFormat
    loggers: Dict[str, Any] = field(default_factory=dict)


class Handler:
    """ Класс обработчика логирования. """
    name: str
    formatter: Dict[str, str]

    def handler(self, level: str) -> Dict[str, str]:
        """ Метод-обработчик логирования. """
        return {
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
            "formatter": self.name,
            "level": level,
        }


class ConsoleHandler(Handler):
    """ Класс обработчик логирования в консоль """
    name = "console"
    fields = (
        "%(levelname)-8s",
        "%(name)-40s",
        "%(module)-20s",
        "%(lineno)-4d",
        "%(message)s",
    )

    formatter = {
        "format": " ".join(fields),
        "datefmt": "%H:%M:%S",
    }


class JsonHandler(Handler):
    """ Класс обработчик логирования в формате json. """
    name = "json"
    fields = (
        "%(correlation_id)s",
        "%(levelname)s",
        "%(version)s",
        "%(module)s",
        "%(lineno)s",
        "%(name).256s",
        "%(message).512s",
        "%(created)s",
        "%(stack_trace).2048s",
    )

    formatter = {
        "class": "json_formatter.JsonFormatter",
        "format": " ".join(fields),
    }


def handler_factory(formatting: LogFormat) -> Handler:
    """
        Метод-фабрика обработчиков логирования.

        Arguments:
            - formatting: Формат логирования.

        Returning:
            Готовый хендлер логирования.
    """
    if formatting == LogFormat.JSON:
        return JsonHandler()

    return ConsoleHandler()
