import sqlalchemy as sqla

from ..structures import Dialect
from ..tools import DI


def edit_distance(*args, **kwargs) -> sqla.Function:
    engine = DI.get(sqla.Engine)
    if engine.dialect.name == Dialect.SQLITE:
        return sqla.func.editdist3(*args, **kwargs)
