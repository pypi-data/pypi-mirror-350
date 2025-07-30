""" Модуль для описания базовой сериализации для http клиента. """

import abc
from typing import (
    Generic,
    TypeVar,
)


TInput = TypeVar("TInput")
TOutput = TypeVar("TOutput")


class BaseSerializer(Generic[TInput, TOutput], abc.ABC):
    """ Класс базовой сериализации. """
    @classmethod
    @abc.abstractmethod
    def serialize(cls, response: TInput) -> TOutput:
        """
            Абстрактный метод сериализации ответа на запрос.

            Arguments:
                - response: Ответ на запрос.

            Returning:
                Сериализованный ответ.
        """
        raise NotImplementedError(
            "Вам необходимо имплементировать метод сериализации в своем сериализаторе",
        )

    @classmethod
    @abc.abstractmethod
    def get_status_code(cls, response: TInput) -> int:
        """
            Абстрактный метод получения кода ответа.

            Arguments:
                - response: Ответ на запрос.

            Returning:
                Код статуса ответа.
        """
        raise NotImplementedError(
            "Вам необходимо имплементировать метод get_status_code в своем сериализаторе",
        )

    @classmethod
    @abc.abstractmethod
    def get_raw_text(cls, response: TInput) -> str:
        """
            Абстрактный метод получения строки текста из ответа на запрос.

            Arguments:
                - response: Ответ на запрос.
            
            Returning:
                Полученное из ответа на запрос текстовое представление.
        """
        raise NotImplementedError(
            "Вам необходимо имплементировать метод get_raw_text в своем сериализаторе",
        )
