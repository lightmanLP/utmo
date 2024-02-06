from typing import TYPE_CHECKING, Any

from ..structures import LIBS_PATH
from ..config import config
from ..tools import event_mngr

if TYPE_CHECKING:
    import sqlite3

SQLITE_EXTS_PATH = LIBS_PATH / "sqlite_exts"


@event_mngr.on("core.db.connect.sqlite")
def load_sqlite_extensions(dbapi_connection: "sqlite3.Connection", connection_record: Any):
    dbapi_connection.enable_load_extension(True)
    for i in SQLITE_EXTS_PATH.iterdir():
        if i.is_file():
            dbapi_connection.load_extension(str(i.resolve()))
    dbapi_connection.enable_load_extension(False)


if config.db.use_builtin_sqlite:
    SQLITE_PATH = (LIBS_PATH / "sqlite3.dll").resolve()
    assert SQLITE_PATH.exists() and SQLITE_PATH.is_file()
    from ctypes import cdll
    cdll.LoadLibrary(str(SQLITE_PATH))
