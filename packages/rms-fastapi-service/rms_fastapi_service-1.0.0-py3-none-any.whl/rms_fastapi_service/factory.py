""" Модуль с реализацией фабрики FastAPI для сервиса. """

from logging import getLogger
from typing import (
    Any,
    Dict,
    List,
    Optional,
    Sequence,
)

from fastapi import APIRouter
from fastapi.responses import ORJSONResponse

from rms_fastapi_service.exceptions import FastApiServiceUsageError
from rms_fastapi_service.healthchecks import (
    BaseHealthCheck,
    get_healthcheck_router,
)
from rms_fastapi_service.logs import LoggingConfig
from rms_fastapi_service.logs.log_config import init as setup_logging
from rms_fastapi_service.registry import (
    DEFAULT_EXCEPTION_HANDLERS,
    DEFAULT_LOG_CONFIG,
    DEFAULT_MIDDLEWARES,
)
from rms_fastapi_service.schemas import (
    ServiceExceptionHandler,
    ServiceMiddleware,
)
from rms_fastapi_service.sentry_setup import setup_sentry
from rms_fastapi_service.server import FastAPIServer
from rms_fastapi_service.utils import to_snakecase
from rms_fastapi_service.version.router_version import get_version_router


logger = getLogger(__name__)


class FastAPIFactory:  # noqa: WPS214
    """ Класс фабрика для конфигурации приложений FastAPI. """
    def __init__(self, app_name: str, app_version: str) -> None:
        self._app_name = to_snakecase(app_name)
        self._app_version = app_version
        self._logconfig: Optional[LoggingConfig] = None
        self._routes: List[APIRouter] = []
        self._middlewares: List[ServiceMiddleware] = []
        self._exception_handlers: List[ServiceExceptionHandler] = []
        self._sentry_dsn: Optional[str] = None
        self._server_checks: Dict[str, Any] = {}
        self._is_with_sentry_called = False

    def with_logconfig(self, logconfig: LoggingConfig) -> "FastAPIFactory":
        """
            Метод определения конфига логирования.

            Arguments:
                - logconfig: Конфигурация логирования.

            Returning:
                Измененная фабрика.
        """
        self._logconfig = logconfig
        return self

    def with_default_logconfig(self) -> "FastAPIFactory":
        """
            Метод определения конфига логирования по умолчанию.

            Returning:
                Измененная фабрика с конфигурацией логирования по умолчанию.
        """
        if self._logconfig:
            return self
        return self.with_logconfig(DEFAULT_LOG_CONFIG)

    def with_sentry(self, sentry_dsn: Optional[str] = None) -> "FastAPIFactory":
        """
            Метод определения senry сервиса.

            Arguments:
                - sentry_dsn: Адрес sentry.

            Returning:
                Измененная фабрика с сентри.
        """
        self._is_with_sentry_called = True
        self._sentry_dsn = sentry_dsn
        return self

    def with_routes(self, *routes: APIRouter) -> "FastAPIFactory":
        """
            Метод определения роутов сервиса.

            Arguments:
                - routes: Роуты сервиса.

            Returning:
                Измененная фабрика.
        """
        self._routes.extend(routes)
        return self

    def with_middlewares(
        self,
        middlewares: Sequence[ServiceMiddleware],
    ) -> "FastAPIFactory":
        """
            Метод определения мидлвара сервиса.

            Arguments:
                - middlewares: Список мидлваров.

            Returning:
                Измененная фабрика.
        """
        self._middlewares.extend(middlewares)
        return self

    def with_default_middlewares(self) -> "FastAPIFactory":
        """
            Метод определения мидлваров сервиса по умолчанию.

            Returning:
                Измененная фабрика.
        """
        return self.with_middlewares(DEFAULT_MIDDLEWARES)

    def with_exception_handlers(
        self,
        exception_handlers: Sequence[ServiceExceptionHandler],
    ) -> "FastAPIFactory":
        """
            Метод определения обработчиков ошибок сервиса.

            Arguments:
                - exception_handler: Данные обработчиков ошибок.

            Returning:
                Измененная фабрика.
        """
        self._exception_handlers.extend(exception_handlers)
        return self

    def with_default_exception_handlers(self) -> "FastAPIFactory":
        """
            Метод определения обработчиков ошибок по умолчанию.

            Arguments:
                - logconfig: Конфигурация логирования.

            Returning:
                Измененная фабрика.
        """
        return self.with_exception_handlers(DEFAULT_EXCEPTION_HANDLERS)

    def with_health_checks(
        self,
        health_checks: Optional[Sequence[BaseHealthCheck]] = None,
        route: str = "/health",
        hide_from_swagger: bool = True,
    ) -> "FastAPIFactory":
        """
            Метод определения проверок работоспособности.

            Arguments:
                - health_checks: Описание проверок работоспособности;
                - route: Роут для проверок;
                - hide_from_swagger: Флаг, определяющий сокрытие от сваггера.

            Returning:
                Измененная фабрика.
        """
        return self._with_server_checks(
            server_checks=health_checks,
            route=route,
            hide_from_swagger=hide_from_swagger,
        )

    def with_ready_checks(
        self,
        ready_checks: Optional[Sequence[BaseHealthCheck]] = None,
        route: str = "/ready",
        hide_from_swagger: bool = True,
    ) -> "FastAPIFactory":
        """
            Метод определения проверок готовности.

            Arguments:
                - ready_checks: Описание проверок готовности;
                - route: Роут для проверок;
                - hide_from_swagger: Флаг, определяющий сокрытие от сваггера.

            Returning:
                Измененная фабрика.
        """
        return self._with_server_checks(
            server_checks=ready_checks,
            route=route,
            hide_from_swagger=hide_from_swagger,
        )

    def with_version_view(
        self,
        route: str = "/version",
        hide_from_swagger: bool = True,
        version: Optional[str] = None,
    ) -> "FastAPIFactory":
        """
            Метод определения описание версии представлений.

            Arguments:
                - route: Роут для версионирования;
                - hide_from_swagger: Флаг, определяющий сокрытие от сваггера;
                - version: Указываемая версия.

            Returning:
                Измененная фабрика.
        """
        return self._with_version_view(
            version=version or self._app_version,
            route=route,
            hide_from_swagger=hide_from_swagger,
        )

    def build(self, app: Optional[FastAPIServer] = None) -> FastAPIServer:
        """
            Метод сборки сервера.

            Arguments:
                - app: Экземпляр приложения FastAPI.

            Returning:
                Собранный сервер FastAPI.
        """
        app = self._define_app(app)
        self._setup_logger()
        # self._setup_metrics(app)
        self._setup_sentry()
        self._setup_routers(app)
        self._setup_middlewares(app)
        self._setup_exception_handlers(app)
        return app

    def build_default(self, app: Optional[FastAPIServer] = None) -> FastAPIServer:
        """
            Метод сборки приложения c настройками по умолчанию.

            Arguments:
                - app: Экземпляр приложения FastAPI.

            Returning:
                Собранный сервер FastAPI.
        """
        self.with_default_logconfig()
        self.with_default_middlewares()
        self.with_default_exception_handlers()
        self.with_health_checks()
        self.with_ready_checks()
        self.with_version_view()
        return self.build(app)

    def _define_app(self, app: Optional[FastAPIServer]) -> FastAPIServer:
        """
            Метод определения приложения FastAPI.

            Arguments:
                - app: Экземпляр приложения FastAPI.

            Returning:
                Экземпляр приложения FastAPI.
        """
        if app is None:
            return FastAPIServer(
                title=self._app_name,
                default_response_class=ORJSONResponse,
                version=self._app_version,
            )
        return app

    def _setup_logger(self) -> None:
        """ Метод настройки и установки логгирования для приложения. """
        if self._logconfig:
            setup_logging(
                config=self._logconfig,
                name=self._app_name,
                version=self._app_version,
            )

    # def _setup_metrics(self, app: FastAPIServer) -> None:
    #     """
    #         Метод настройки и установки метрик для приложения.

    #         Arguments:
    #             - app: Экземпляр приложения FastAPI.
    #     """
    #     DefaultMetrics().setup(app, self._app_name)
    #     MetricsCollector.set_app_name(name=self._app_name)

    def _setup_routers(self, app: FastAPIServer) -> None:
        """
            Метод настройки и установки роутов для приложения.

            Arguments:
                - app: Экземпляр приложения FastAPI.
        """
        for router in self._routes:
            app.include_router(router)

    def _setup_middlewares(self, app: FastAPIServer) -> None:
        """
            Метод настройки и установки мидлваров для приложения.

            Arguments:
                - app: Экземпляр приложения FastAPI.
        """
        for middleware in self._middlewares:
            # При версии fastapi>=0.109 появляется ошибка тайпинга
            app.add_middleware(middleware.middleware_class, **middleware.options)  # type: ignore

    def _setup_exception_handlers(self, app: FastAPIServer) -> None:
        """
            Метод настройки и установки обработчиков ошибок для приложения.

            Arguments:
                - app: Экземпляр приложения FastAPI.
        """
        for handler in self._exception_handlers:
            app.add_exception_handler(handler.exception, handler.handler)

    def _setup_sentry(self) -> None:
        """
            Метод настройки и установки senry для приложения.

            Arguments:
                - app: Экземпляр приложения FastAPI.
        """
        if not self._is_with_sentry_called:
            raise FastApiServiceUsageError("Необходимо вызвать метод with_sentry()"
                                      "перед сборкой приложения.")
        setup_sentry(self._sentry_dsn)

    def _with_server_checks(
        self,
        server_checks: Optional[Sequence[BaseHealthCheck]],
        route: str,
        hide_from_swagger: bool,
    ) -> "FastAPIFactory":
        """
            Внутренний метод установки серверных проверок.

            Arguments:
                - server_checks: Описание серверных проверок;
                - route: Роут для проверок;
                - hide_from_swagger: Флаг, определяющий сокрытие от сваггера.

            Returning:
                Измененная фабрика.
        """
        if route in self._server_checks:
            logger.warning("Роут \"%s\" уже был добавлен.", route)
            return self

        self.with_routes(
            get_healthcheck_router(
                health_checks=server_checks if server_checks else [],
                route=route,
                hide_from_swagger=hide_from_swagger,
            ),
        )
        self._server_checks[route] = server_checks
        return self

    def _with_version_view(
        self,
        version: str,
        route: str,
        hide_from_swagger: bool,
    ) -> "FastAPIFactory":
        """
            Внутренний метод установки версий представлений.

            Arguments:
                - version: Устанавливаемая версия;
                - route: Роут, на который указывается версия;
                - hide_from_swagger: Флаг, определяющий сокрытие от сваггера.

            Returning:
                Измененная фабрика.
        """
        self.with_routes(
            get_version_router(
                version=version,
                route=route,
                hide_from_swagger=hide_from_swagger,
            ),
        )
        return self
