""" Модуль для настройки и работы с senry. """

import logging
from typing import Optional

import sentry_sdk
from sentry_sdk.integrations.asyncio import AsyncioIntegration
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.starlette import StarletteIntegration


def setup_sentry(sentry_dsn: Optional[str]) -> None:
    """
        Метод настройки сентри для сервера.

        Arguments:
            - sentry_dsn: Адрес сервера сентри.
    """
    if sentry_dsn is None:
        logging.warning("Sentry DSN is not set")
        return

    sentry_sdk.init(
        dsn=sentry_dsn,
        attach_stacktrace=True,
        integrations=[
            StarletteIntegration(transaction_style="url"),
            FastApiIntegration(transaction_style="url"),
            AsyncioIntegration(),
        ],
    )
