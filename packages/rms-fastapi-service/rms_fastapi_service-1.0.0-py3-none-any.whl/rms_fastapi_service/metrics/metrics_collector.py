""" Модуль реализации метрик сервера FastAPI. """

from typing import (
    Any,
    ContextManager,
    Dict,
    Iterable,
    List,
    Optional,
    Tuple,
)

from prometheus_client import (
    Counter,
    Gauge,
    Histogram,
)

from rms_fastapi_service.utils import to_snakecase


class MetricsCollector:  # noqa: WPS214, WPS338
    """ Класс-коллектор всех метрик сервиса. """
    __instance = None

    def __new__(cls, *args: Any, **kwargs: Any) -> "MetricsCollector":
        if cls.__instance is None:
            cls.__instance = super().__new__(cls, *args, **kwargs)  # noqa: WPS601
            cls.__instance._metrics = {}  # noqa: WPS437
        return cls.__instance

    _app_name: str = ""

    def __init__(self) -> None:
        self._metrics: Dict[str, Any]

    @classmethod
    def set_app_name(cls, name: str) -> None:  # noqa: WPS615
        """
            Метод определения названия приложения.

            Arguments:
                - name: Название приложения.
        """
        cls._app_name = to_snakecase(name)  # noqa: WPS601

    def db_hist(self, db: str, method: str) -> ContextManager[Histogram]:
        """
            Метод создания гистограммы по времени выполнения запроса для базы данных.

            Arguments:
                - db: Название базы данных;
                - method: Метод запроса к БД.

            Returning:
                Контекстный менеджер гистограммы БД.
        """
        metric = self.hist(
            name="db_query_duration_seconds",
            docs="Время выполнения запросов к БД",
            labels=("db", "method"),
        )
        return metric.labels(db=db, method=method).time()

    def task_hist(self, strategy: str, method: str) -> ContextManager[Histogram]:
        """
            Метод создания гистограммы по времени выполнения запроса для задач.

            Arguments:
                - strategy: Название задачи;
                - method: Метод выполняемой задачи.

            Returning:
                Контекстный менеджер гистограммы задачи.
        """
        metric = self.hist(
            name="task_duration",
            docs="Время выполнения задачи",
            labels=("name", "method"),
        )
        return metric.labels(name=strategy, method=method).time()

    def client_hist(
        self,
        service: str,
        method: str,
        name: str,
    ) -> ContextManager[Histogram]:
        """
            Метод создания гистограммы для клиента по времени выполнения запроса.

            Arguments:
                - service: Сервис, к которому обращается клиент;
                - method: Метод обработки;
                - name: Название клиента.

            Returning:
                Контекстный менеджер гистограммы клиента.
        """
        metric = self.hist(
            name="http_client_query_duration_seconds",
            docs="Время запрос http клиента",
            labels=("service", "method", "name"),
        )
        return metric.labels(service=service, method=method, name=name).time()

    def client_counter(self, service: str, method: str, name: str, status: int) -> None:
        """
            Метод создания счетчика клиента.

            Arguments:
                - service: Сервис, к которому обращается клиент;
                - method: Метод обработки;
                - name: Название клиента.
        """
        metric = self.counter(
            name="http_client_status_count",
            docs="Счетчик клиентов http",
            labels=("service", "method", "name", "status"),
        )
        metric.labels(service=service, method=method, name=name, status=status).inc()

    def status_counter(self, method: str, name: str, status: int) -> None:
        """
            Метод создания счетчика статуса http.

            Arguments:
                - method: Метод обработки;
                - name: Название клиента;
                - status: Код статус http.
        """
        metric = self.counter(
            name="status_request_count",
            docs="Счетчик статуса http",
            labels=("method", "name", "status"),
        )
        metric.labels(method=method, name=name, status=status).inc()

    def error_code_counter(self, method: str, name: str, error_code: str) -> None:
        """
            Метод создания счетчика кодов с ошибками.

            Arguments:
                - method: Метод обработки;
                - name: Название клиента;
                - error_code: Код ошибки http.
        """
        metric = self.counter(
            name="error_code_request_count",
            docs="Счетчик кодов с ошибками",
            labels=("method", "name", "error_code"),
        )
        metric.labels(method=method, name=name, error_code=error_code).inc()

    def count_handler_statuses(self, handler_name: str, status: int) -> None:
        """
            Метод создания счетчика статусов http обработчика.

            Arguments:
                - handler_name: Название обработчика;
                - status: Код статус http.
        """
        counter = self.counter(
            name=f"{handler_name.lower()}_status_request_count",
            docs="Счетчик http статусов обработчика",
            labels=["status"],
        )
        counter.labels(status=status).inc()

    def count_handler_errors(self, handler_name: str, error_code: str) -> None:
        """
            Метод создания счетчика ошибок обработчика.

            Arguments:
                - handler_name: Название обработчика;
                - error_code: Код ошибки http.
        """
        metric = self.counter(
            name=f"{handler_name.lower()}_error_code_request_count",
            docs="Счетчик кодов с ошибками обработчика",
            labels=["error_code"],
        )
        metric.labels(error_code=error_code).inc()

    def hist(
        self,
        name: str,
        docs: str,
        labels: Iterable[str],
        buckets: Tuple[float, ...] = Histogram.DEFAULT_BUCKETS,
    ) -> Histogram:
        """
            Метод создания гистограммы.

            Arguments:
                - name: Название гистограммы;
                - docs: Док строка гистограммы (ее описание);
                - labels: Лейблы на гистограмме;
                - buckets: Бакеты на гистограмме.

            Returning:
                Подготовленная гистограмма.
        """
        metric = self._metrics.get(name)
        if not metric:
            metric = Histogram(
                name=name,
                documentation=docs,
                labelnames=labels,
                namespace=self._app_name,
                unit="seconds",
                buckets=buckets,
            )
            self._metrics[name] = metric
        return self._metrics[name]

    def counter(self, name: str, docs: str, labels: Iterable[str]) -> Counter:
        """
            Метод создания счетчика.

            Arguments:
                - name: Название счетчика;
                - docs: Док строка счетчика (его описание);
                - labels: Лейблы счетчика.

            Returning:
                Подготовленный счетчик.
        """
        metric = self._metrics.get(name)
        if not metric:
            metric = Counter(
                name=name,
                documentation=docs,
                namespace=self._app_name,
                labelnames=labels,
            )
            self._metrics[name] = metric
        return metric

    def gauge(self, name: str, docs: str, labels: Optional[List[str]] = None) -> Gauge:
        """
            Метод создания измерителя.

            Arguments:
                - name: Название измерителя;
                - docs: Док строка измерителя (его описание);
                - labels: Лейблы измерителя.

            Returning:
                Подготовленный измеритель.
        """
        metric = self._metrics.get(name)
        if not metric:
            metric = Gauge(
                name=name,
                documentation=docs,
                namespace=self._app_name,
                labelnames=labels or [],
            )
            self._metrics[name] = metric
        return metric

    @property
    def metrics(self) -> Dict[str, Any]:
        """Свойство получения метрик коллектора. """
        return self._metrics
