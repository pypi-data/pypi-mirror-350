""" Модуль для работы с ответами от сервиса FastAPI в схемах. """

from typing import (
    Any,
    Dict,
    List,
    Optional,
    Union,
)

from pydantic import (
    BaseModel,
    Field,
)


class ErrorMessage(BaseModel):
    """ Класс сообщения об ошибке. """
    error_code: Optional[int] = Field(
        default=None,
        description="Код ошибки",
    )
    message: str = Field(
        default="Internal Server Error",
        description="Сообщение об ошибке",
    )

    @classmethod
    def from_pydantic_error(
        cls,
        err: Dict[str, Any],
    ) -> "ErrorMessage":
        """
            Метод установки кода и сообщения ошибки.

            Arguments:
                - err: Данные об ошибке.

            Returning:
                Экземпляр сообщения об ошибке с установленными данными.
        """
        return cls(
            message=(
                f"""Validation error: {err.get("msg")}. """
                f"""Loc: {err.get("loc")}. """
                f"""Type: {err.get("type")}."""
            ),
        )


class ErrorResponse(BaseModel):
    """ Класс для работы с ошибками в ответе. """
    success: bool = False
    errors: Optional[List[ErrorMessage]] = Field(
        description="Соообщения об ошибках",
        default=[],
    )


class BaseResponse(BaseModel):
    """ Класс для работы базовым ответом от сервиса. """
    success: Optional[bool] = True
    answer: Union[Dict[str, Any], BaseModel, str, List[Any]] = Field(
        description="Целевой ответ от сервиса",
    )
    errors: Optional[List[ErrorMessage]] = Field(
        description="Соообщения об ошибках",
        default=[],
    )
