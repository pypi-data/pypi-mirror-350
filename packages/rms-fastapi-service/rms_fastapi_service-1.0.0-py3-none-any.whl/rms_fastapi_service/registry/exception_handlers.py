""" Модуль для обработчика ошибок в сервисе FastAPI для регистри. """

from fastapi.exceptions import (
    RequestValidationError,
    ResponseValidationError,
)
from pydantic import ValidationError

from rms_fastapi_service.exceptions import (
    ServiceExceptionError,
    general_exception_handler,
    service_exception_handler,
    validation_exception_handler,
)
from rms_fastapi_service.schemas import ServiceExceptionHandler


DEFAULT_EXCEPTION_HANDLERS = (
    ServiceExceptionHandler(
        exception=RequestValidationError,
        handler=validation_exception_handler,
    ),
    ServiceExceptionHandler(
        exception=ResponseValidationError,
        handler=validation_exception_handler,
    ),
    ServiceExceptionHandler(
        exception=ValidationError,
        handler=validation_exception_handler,
    ),
    ServiceExceptionHandler(
        exception=ServiceExceptionError,
        handler=service_exception_handler,
    ),
    ServiceExceptionHandler(exception=Exception, handler=general_exception_handler),
)
