""" Модуль инициализации пакета метрик для сервера FastAPI. """

from rms_fastapi_service.metrics.metrics_collector import MetricsCollector
from rms_fastapi_service.metrics.default_metrics import DefaultMetrics


__all__ = (
    "DefaultMetrics",
    "MetricsCollector",
)
