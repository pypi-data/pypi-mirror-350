""" Модуль базовых типов http клиента. """

import typing as tp
from enum import Enum


PingResult = tp.Tuple[bool, str]
Json = tp.Union[
    int,
    str,
    bool,
    tp.List[tp.Any],
    tp.Mapping[str, tp.Any],
]
Headers = tp.Dict[str, tp.Any]
Params = tp.Dict[str, tp.Any]
FileContent = tp.Union[tp.IO[bytes], bytes]
FileTypes = tp.Union[
    FileContent,
    tp.Tuple[tp.Optional[str], FileContent],
    tp.Tuple[tp.Optional[str], FileContent, tp.Optional[str]],
    tp.Tuple[
        tp.Optional[str],
        FileContent,
        tp.Optional[str],
        tp.Mapping[str, str],
    ],
]
RequestFiles = tp.Union[
    tp.Mapping[str, FileTypes],
    tp.Sequence[tp.Tuple[str, FileTypes]],
]


class HTTPMethods(str, Enum):  # noqa: WPS600
    """ Класс описания методов http запроса. """
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"
