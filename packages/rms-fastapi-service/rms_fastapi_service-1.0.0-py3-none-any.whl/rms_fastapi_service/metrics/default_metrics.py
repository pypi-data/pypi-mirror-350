""" Модуль для работы с метриками по умолчанию. """

from typing import (
    Callable,
    List,
    Optional,
    Union,
)

from fastapi import FastAPI
from prometheus_fastapi_instrumentator import (
    Instrumentator,
    metrics,
)


class DefaultMetrics:
    """ Класс для работы с метриками по умолчанию (стандартными). """
    def __init__(self, instrumentator: Optional[Instrumentator] = None) -> None:
        if instrumentator is None:
            instrumentator = Instrumentator(should_group_status_codes=False)
        self.instrumentator = instrumentator

    def setup(self, app: FastAPI, app_name: str) -> None:
        """
            Метод настройки метрик по умолчанию.

            Arguments:
                - app: Приложение FastAPI;
                - app_name: Название приложения.
        """
        default_metrics = self._set_default_metrics(app_name=app_name)
        for metric in default_metrics:
            self.instrumentator.add(metric)
        self.instrumentator.instrument(app=app).expose(app=app, include_in_schema=False)

    def _set_default_metrics(
        self,
        app_name: str,
    ) -> List[Union[Callable[[metrics.Info], None], None]]:
        """
            Метод установки метрик по умолчанию.

            Arguments:
                - app_name: Название приложения.

            Returning:
                Список подготовленных для приложения метрик по умолчанию.
        """
        return [
            metrics.latency(
                metric_name="api_request_duration_seconds",
                metric_namespace=app_name,
                should_include_method=True,
                should_include_status=True,
            ),
            metrics.requests(
                metric_name="status_request_count",
                metric_namespace=app_name,
                should_include_method=True,
                should_include_status=True,
            ),
        ]
