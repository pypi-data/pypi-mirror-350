""" Модуль, содержащий вспомогательные функции сервиса FastAPI. """

import os
from pathlib import Path
from typing import (
    Any,
    Dict,
    Union,
)

from pyhocon import ConfigFactory


def to_snakecase(inp: str) -> str:
    """
        Метод приведения строки к стилю snakecase.

        Arguments:
            - inp: Произвольная строка, которую нужно привести к snakecase.

        Returning:
            Преобразованная в snakecase строка.
    """
    snake_case = "_"
    to_replace = (" ", "-")
    result = inp.lower()
    for old_case in to_replace:
        result = result.replace(old_case, snake_case)

    return result


def config_factory(
    folder: Union[str, Path],
    env_var: str = "ENV",
    section: str = "config",
) -> Dict[str, Any]:
    """
        Метод, реализующий фабрику конфига.
        По данным настроек формирует конфигурацию приложения.

        Arguments:
            - folder: Папка, из которой вычитываются настройки для конфигурации;
            - env_var: Переменная, которая определяет выбираемое окружение;
            - section: Секция в настройках, которую необходимы взять для конфигурации.

        Returning:
            Объект конфигурации приложения.
    """
    package_dir = Path(folder)
    env = os.getenv(env_var, "default")
    conf_path = package_dir / f"{env}.conf"
    fallback_conf_path = package_dir / "default.conf"

    factory = ConfigFactory.parse_file(conf_path)
    factory = factory.with_fallback(fallback_conf_path)
    config = factory.get_config(section).as_plain_ordered_dict()

    # Проверка на нулевые поля
    return {cfg_var: cfg_val for cfg_var, cfg_val in config.items() if bool(cfg_val)}
