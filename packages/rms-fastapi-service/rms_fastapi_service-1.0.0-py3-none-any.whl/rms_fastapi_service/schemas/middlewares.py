""" Модуль для работы с мидлваром в схемах FastAPI. """

from typing import (
    Any,
    Dict,
    Type,
    Union,
)

from pydantic import (
    BaseModel,
    Field,
)
from starlette.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware


class ServiceMiddleware(BaseModel, arbitrary_types_allowed=True):
    """ Базовый класс мидлвара сервиса. """
    middleware_class: Type[Union[BaseHTTPMiddleware, Middleware, Any]] = Field(
        description="Класс мидлвара",
    )
    options: Dict[str, Any] = Field(
        description=(
            "Опции мидлавара. key - название аргумента мидлавара, "
            "value - реализация мидлвара или его параметры."
        ),
    )
