""" Модуль для работы с инджектированием. """

import contextvars
from logging import (
    LogRecord,
    getLogRecordFactory,
    setLogRecordFactory,
)
from typing import (
    Any,
    Iterable,
)


def inject_version(version: str) -> None:
    """
        Метод инъекции версии.

        Arguments:
            - version: Версия для инъекции.
    """
    old_factory = getLogRecordFactory()

    def version_log_factory(*args: Any, **kwargs: Any) -> LogRecord:  # noqa: WPS430
        record = old_factory(*args, **kwargs)
        record.version = version
        return record

    setLogRecordFactory(version_log_factory)


def inject_contextvars(fields: Iterable[str]) -> None:
    """
        Метод инъекции переменных контекста.

        Arguments:
            - fields: Переменные контекста.
    """
    old_factory = getLogRecordFactory()

    def contextvars_log_factory(*args: Any, **kwargs: Any) -> LogRecord:  # noqa: WPS430
        record = old_factory(*args, **kwargs)
        ctx = contextvars.copy_context()
        log_ctx = {
            log_field.name: value for log_field, value in ctx.items() if log_field.name in fields
        }

        for log_field in fields:
            setattr(record, log_field, log_ctx.get(log_field))

        return record

    setLogRecordFactory(contextvars_log_factory)
