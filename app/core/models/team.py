from typing import TYPE_CHECKING
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models import Base
from core.models.mixins.id_int_pk import IdIntPkMixin
from core.models.mixins.time_stamp import TimeStampMixin

if TYPE_CHECKING:
    from core.models import User


class Team(
    Base,
    IdIntPkMixin,
    TimeStampMixin,
):
    name: Mapped[str] = mapped_column(String, unique=True)
    description: Mapped[str | None] = mapped_column(String, default=None)
    code: Mapped[str] = mapped_column(String, unique=True)

    admin_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    users: Mapped[list["User"]] = relationship(
        back_populates="team",
        passive_deletes=True,
    )
