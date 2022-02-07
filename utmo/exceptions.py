class BaseException(Exception):
    ...


class UnsupportedPlatformError(Exception):
    def __init__(self, platform: str = "platform") -> None:
        super().__init__(f"{platform} not supported")


class UnsupportedDBDialectError(Exception):
    def __init__(self, dialect: str = "dialect") -> None:
        super().__init__(f"{dialect} not supported (use postgres or sqlite)")


class ConfigParseError(BaseException):
    def __init__(self, info: str = "config can't be parsed") -> None:
        super().__init__(info)
