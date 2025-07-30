""" Модуль для работы с корреляциями. """

from contextvars import ContextVar
from typing import Any
from uuid import uuid4

from fastapi import Request
from starlette.middleware.base import RequestResponseEndpoint
from starlette.responses import Response


CTX_CORRELATION_ID: ContextVar[str] = ContextVar("correlation_id")
CONST_CORRELATION_ID = "x-correlation-id"


async def correlation_middleware(
    req: Request,
    call_next: RequestResponseEndpoint,
) -> Response:
    """
        Метод выделения и мидлвар обработки коллеряции.

        Arguments:
            - req: Полный запрос;
            - callnext: Конечная точка, на которую необходимо отправить ответ.

        Returning:
            Обновленный запрос.
    """
    req.state.correlation_id = req.headers.get(CONST_CORRELATION_ID, uuid4().hex)
    CTX_CORRELATION_ID.set(req.state.correlation_id)
    response = await call_next(req)
    response.headers.update({CONST_CORRELATION_ID: req.state.correlation_id})
    return response


def get_correlation_id() -> Any:
    """
        Метод получения идентификатора корреляции.

        Returning:
            Идентификатор корреляции.
    """
    try:
        return CTX_CORRELATION_ID.get()
    except LookupError:
        return None
