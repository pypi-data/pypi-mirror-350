""" Модуль конфигурации http клиента. """

from dataclasses import (
    dataclass,
    field,
)
from typing import (
    Any,
    Optional,
)

from rms_fastapi_service.clients.schema.basic_types import Headers


@dataclass
class HttpClientConf:
    """ Класс конфигурации http клиента. """
    url: str
    timeout: float = field(default=5)
    limit: int = field(default=100)
    bearer: Optional[str] = None
    headers: Optional[Headers] = None
    backoff: float = field(default=0.1)
    ignore_status: bool = field(default=False)
    client_kwargs: dict[str, Any] = field(default_factory=dict)
