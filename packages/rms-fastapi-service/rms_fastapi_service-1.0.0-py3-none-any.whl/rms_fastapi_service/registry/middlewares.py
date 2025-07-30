""" Модуль для работы с мидлваром в регистри FastAPI. """

from starlette.middleware.base import BaseHTTPMiddleware

from rms_fastapi_service.middlewares.correlation import correlation_middleware
from rms_fastapi_service.schemas import ServiceMiddleware


DEFAULT_MIDDLEWARES = (
    ServiceMiddleware(
        middleware_class=BaseHTTPMiddleware,
        options={"dispatch": correlation_middleware},
    ),
)
