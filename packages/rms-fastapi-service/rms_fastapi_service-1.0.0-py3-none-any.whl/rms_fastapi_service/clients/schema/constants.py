""" Модуль константных значений использующихся для реализации http клиента. """

from typing import Final


BACKOFF: Final[float] = 1.5
MAX_BACKOFF: Final[float] = 10

HTTP_SUCCESS_CODE: Final[int] = 200
HTTP_LOW_SUCCESS_CODE: Final[int] = HTTP_SUCCESS_CODE
HTTP_HIGH_SUCCESS_CODE: Final[int] = 299
