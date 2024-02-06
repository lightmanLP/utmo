from typing import Any

from ..exceptions import BaseException


class InjectionError(BaseException):
    def __init__(self, key: Any) -> None:
        super().__init__(f"'{key}' instance is inaccessible")
