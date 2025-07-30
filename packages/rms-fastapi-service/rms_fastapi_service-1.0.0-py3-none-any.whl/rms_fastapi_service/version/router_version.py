""" Модуль для работы с версией по роуту. """

import typing as tp

from fastapi import APIRouter

from rms_fastapi_service.version.version_response import VersionResponse


def get_version_router(
    version: str,
    route: tp.Optional[str] = None,
    hide_from_swagger: bool = True,
) -> APIRouter:
    """
        Метод установления версии роута.

        Arguments:
            - version: Указание версии;
            - route: Роут, по которому необходимо поставить версию;
            - hide_from_swagger: Флаг, определяющий сокрытие от свагера.

        Returning:
            Роутер с установленным роутом и версией.
    """
    if route is None:
        route = "/version"
    router = APIRouter(tags=["version"], include_in_schema=not hide_from_swagger)

    @router.get(route)
    async def handler() -> VersionResponse:  # noqa: WPS430
        return VersionResponse(version=version,)

    return router
