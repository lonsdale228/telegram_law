from aiogram import Dispatcher
from .throttling import ThrottlingMiddleware


__all__ = [
    "ThrottlingMiddleware",
    "setup"
]


def setup(dp: Dispatcher) -> None:
    for m in [
        ThrottlingMiddleware()
    ]:
        dp.message.middleware(m)