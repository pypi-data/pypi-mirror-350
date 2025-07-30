""" Фабрика для работы с проверками. """

import typing as tp
from logging import getLogger

from fastapi import (
    APIRouter,
    Response,
    status,
)
from pydantic import (
    BaseModel,
    create_model,
)

from rms_fastapi_service.healthchecks.base_healthcheck import BaseHealthCheck


logger = getLogger(__name__)


def generate_model_from_healthchecks(
    health_checks: tp.Sequence[BaseHealthCheck],
) -> tp.Type[BaseModel]:
    """
        Метод генерации модели по проверкам.

        Arguments:
            - health_checks: Набор проверок.

        Returning:
            Базовая модель.
    """
    checkers = {checker.NAME: (bool, True) for checker in health_checks}
    return create_model("Check", **checkers, status=(bool, True))  # type: ignore


def get_healthcheck_router(
    health_checks: tp.Sequence[BaseHealthCheck],
    route: tp.Optional[str] = None,
    hide_from_swagger: bool = True,
) -> APIRouter:
    """
        Метод определения роута для проверок.

        Arguments:
            - health_checks: Набор проверок;
            - route: Роут для проверок;
            - hide_from_swagger: Флаг, определяющий сокрытие от сваггера.

        Returning:
            Роутер с проверками.
    """
    if route is None:
        route = "/ready"
    model = generate_model_from_healthchecks(health_checks)
    router = APIRouter(tags=["healthcheck"], include_in_schema=not hide_from_swagger)

    @router.get(route)
    async def handler(response: Response) -> model:  # type: ignore # noqa: WPS430
        checks: tp.Dict[str, bool] = {"status": True}
        for checker in health_checks:
            check_status = False
            try:
                check_status = await checker.is_health()
            except BaseException:  # noqa: WPS424
                logger.exception("Health check error")
            checks[checker.NAME] = check_status
            if not check_status:
                checks["status"] = False
                response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return model(**checks)

    return router
