""" Модуль версионирования ответа на запрос. """

from pydantic import BaseModel


class VersionResponse(BaseModel):
    """ Класс для работы с версией ответа. """
    version: str
