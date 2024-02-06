from typing import Generic, TypeVar, Any
from enum import IntEnum

import sqlalchemy as sqla

IntEnumT = TypeVar("IntEnumT", bound=IntEnum)


class IntEnumType(sqla.TypeDecorator, Generic[IntEnumT]):
    impl = sqla.Integer
    enum: type[IntEnumT]

    def __init__(self, enumtype: type[IntEnumT], *args, **kwargs) -> None:
        self.enum = enumtype
        super().__init__(*args, **kwargs)

    def process_bind_param(
        self,
        value: int | IntEnumT,
        dialect: Any
    ) -> int | None:
        if isinstance(value, self.enum):
            return value.value
        return value

    def process_result_value(
        self,
        value: int | IntEnumT,
        dialect: Any
    ) -> IntEnumT | None:
        if value is None:
            return None
        elif isinstance(value, self.enum):
            return value
        return self.enum(value)

    def coerce_compared_value(self, op: Any, value: Any) -> Any:
        if value is None:
            return None
        elif isinstance(value, int):
            return sqla.Integer()
        else:
            return self


class PathType(sqla.TypeDecorator):
    impl = sqla.Text

    def process_bind_param(
        self,
        value: Any,
        dialect: Any
    ) -> str | None:
        if value is None:
            return ""
        elif isinstance(value, str):
            return value
        return str(value)

    def process_result_value(
        self,
        value: Any,
        dialect: Any
    ) -> int | None:
        if value is None or value == "":
            return None
        elif isinstance(value, int):
            return value
        return int(value)

    def coerce_compared_value(self, op: Any, value: Any) -> Any:
        if value is None:
            return None
        return self
