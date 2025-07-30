""" Модуль проверок баз данных. """

from databases import Database  # noqa: WPS433 # type: ignore


class DatabasesHealthCheck:
    """ Класс для работы с проверками баз данных. """
    def __init__(self, name: str, database: Database):
        self.NAME = name
        self._db = database

    async def is_health(self) -> bool:
        """
            Метод проверки стабильной работы.

            Returning:
                Флаг, определяющий стабильность работы.
        """
        try:
            res = await self._db.execute("select 1")
            return res == 1
        except BaseException:  # noqa: WPS424
            return False
