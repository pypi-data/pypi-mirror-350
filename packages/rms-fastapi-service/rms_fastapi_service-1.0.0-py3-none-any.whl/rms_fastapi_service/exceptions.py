""" Модуль ошибок сервиса FastAPI. """

from typing import (
    List,
    Union,
)

from fastapi import (
    Request,
    status,
)
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import (
    RequestValidationError,
    ResponseValidationError,
)
from fastapi.responses import ORJSONResponse

from rms_fastapi_service.schemas.response import (
    ErrorMessage,
    ErrorResponse,
)


class ServiceExceptionError(Exception):
    """ Класс серверной ошибки FastAPI. """
    def __init__(self, code: int, message: str):
        """
            Метод инициализации серверной ошибки.

            Arguments:
                - code: Код ошибки;
                - message: Сообщение ошибки.
        """
        self.code = code
        self.message = message


class FastApiServiceUsageError(Exception):
    """ Исключение для недопустимого использования сервиса Fast Api """


def error_response(
    status_code: int,
    errors: List[ErrorMessage],
) -> ORJSONResponse:
    """
        Метод создания ответа с ошибками.

        Arguments:
            - status_code: Код ошибки;
            - errors: Список сообщений об ошибках.

        Returning:
            Json ответ с ошибками.
    """
    return ORJSONResponse(
        content=jsonable_encoder(
            ErrorResponse(errors=errors),
        ),
        status_code=status_code,
    )


async def validation_exception_handler(
    _: Request,
    exc: Union[RequestValidationError, ResponseValidationError],
) -> ORJSONResponse:
    """
        Перехватчик ошибок валидации Pydantic.

        Arguments:
            - exc: Валидационная ошибка.

        Returning:
            Json ответ с соответсвующим статусом ошибки в ее описанием.
    """
    validation_errors = [ErrorMessage.from_pydantic_error(error) for error in exc.errors()]
    return error_response(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        errors=validation_errors,
    )


async def general_exception_handler(
    _: Request,
    exc: Exception,
) -> ORJSONResponse:
    """
        Перехватчик общих ошибок.

        Arguments:
            - exc: Общая ошибка.

        Returning:
            Json ответ с соответсвующим статусом ошибки в ее описанием.
    """
    return error_response(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        errors=[ErrorMessage(message=str(exc))],
    )


async def service_exception_handler(
    _: Request,
    exc: ServiceExceptionError,
) -> ORJSONResponse:
    """
        Перехватчик общих ошибок сервера.

        Arguments:
            - exc: Общая серверная ошибка.

        Returning:
            Json ответ с соответсвующим статусом ошибки в ее описанием.
    """
    return error_response(
        status_code=exc.code,
        errors=[
            ErrorMessage(
                error_code=exc.code,
                message=exc.message,
            ),
        ],
    )
