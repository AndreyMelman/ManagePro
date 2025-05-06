from typing import TYPE_CHECKING

from fastapi_users_db_sqlalchemy import (
    SQLAlchemyBaseUserTable,
    SQLAlchemyUserDatabase,
)
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from core.types.user_id import UserIdType
from core.types.role import UserRole
from .base import Base
from .mixins.id_int_pk import IdIntPkMixin
from .mixins.time_stamp import TimeStampMixin

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class User(
    Base,
    IdIntPkMixin,
    TimeStampMixin,
    SQLAlchemyBaseUserTable[UserIdType],
):
    role: Mapped[UserRole] = mapped_column(
        String,
        nullable=False,
        default=UserRole.USER,
    )

    @classmethod
    def get_db(cls, session: "AsyncSession"):
        return SQLAlchemyUserDatabase(session, cls)
