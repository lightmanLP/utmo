class BaseException(Exception):
    ...


class UnsupportedPlatformError(BaseException):
    def __init__(self, platform: str = "platform") -> None:
        super().__init__(f"{platform} not supported")


class UnsupportedDBDialectError(BaseException):
    def __init__(self, dialect: str = "dialect") -> None:
        super().__init__(f"{dialect} not supported (use postgres or sqlite)")
