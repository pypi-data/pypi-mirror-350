""" Модуль проверок типа dummy. """


class DummyHealthCheck:
    """ Класс для работы с проверками типа dummy. """
    NAME: str = "dummy"

    def __init__(self, status: bool = True) -> None:
        self._status = status

    async def is_health(self) -> bool:
        """
            Метод проверки стабильной работы.

            Returning:
                Флаг, определяющий стабильность работы.
        """
        return self._status
