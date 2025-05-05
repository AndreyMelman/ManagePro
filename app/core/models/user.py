from fastapi_users_db_sqlalchemy import (
    SQLAlchemyBaseUserTable,
)

from core.types.user_id import UserIdType
from .base import Base
from .mixins.id_int_pk import IdIntPkMixin
from .mixins.time_stamp import TimeStampMixin


class User(
    Base,
    IdIntPkMixin,
    TimeStampMixin,
    SQLAlchemyBaseUserTable[UserIdType],
):
    pass
