""" Модуль, реализующий сервер FastAPI. """

from typing import (
    Any,
    Dict,
    Optional,
    Union,
)

import uvicorn
from fastapi import FastAPI


class FastAPIServer(FastAPI):
    """ Класс сервера FastAPI """
    def run(
        self,
        *args: Any,
        host: str = "0.0.0.0",  # noqa: S104
        port: int = 8000,
        log_config: Optional[Union[Dict[str, Any], str]] = None,
        **kwargs: Any,
    ) -> None:
        """
            Метод запуска сервера FastAPI.

            Arguments:
                - host: Хост, на котором будет развернут сервер;
                - port: Порт хоста, на котором будет развернут сервер;
                - log_config: Конфигурация логирования сервера.
                - Другие позиционные и ключевые аргументы.
        """
        uvicorn.run(
            self,
            host=host,
            port=port,
            log_config=log_config,
            *args,
            **kwargs,
        )
