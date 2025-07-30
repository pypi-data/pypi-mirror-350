""" Модуль ошибок для http клиента. """

from json import JSONDecodeError


class HTTPTransportError(Exception):
    """ Ошибка транспортного уровня. """


class HTTPTimeoutError(HTTPTransportError):
    """ Ошибка по таймауту. """


class HTTPStatusCodeError(HTTPTransportError):
    """ Неожиданный код статуса. """


class JsonSerializerDecodeError(JSONDecodeError):
    """ Невозможно интерпретировать входящую строку, как JSON. """
