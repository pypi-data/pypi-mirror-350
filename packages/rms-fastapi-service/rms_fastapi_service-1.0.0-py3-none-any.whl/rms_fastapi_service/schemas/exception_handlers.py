""" Модуль для обработчика ошибок в сервисе FastAPI. """

from typing import (
    Any,
    Callable,
    Type,
    Union,
)

from fastapi import Request
from pydantic import (
    BaseModel,
    Field,
)


class ServiceExceptionHandler(BaseModel, arbitrary_types_allowed=True):
    """ Базовый класс обработчика сервисных ошибок. """
    exception: Union[int, Type[Exception]] = Field(description="Класс ошибок")
    handler: Callable[[Request, Any], Any] = Field(description="Обработчик ошибок")
