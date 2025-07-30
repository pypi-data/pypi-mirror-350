""" Модуль, реализующий базовую работу с проверками. """

import typing as tp


class BaseHealthCheck(tp.Protocol):
    """ Базовый класс проверок """
    NAME: str

    async def is_health(self) -> bool:
        """
            Метод проверки стабильной работы.

            Returning:
                Флаг, определяющий стабильность работы.
        """
        ...  # noqa: WPS428
