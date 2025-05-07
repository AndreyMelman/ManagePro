from typing import TYPE_CHECKING
from sqlalchemy import (
    String,
    ForeignKey,
    Text,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from core.models import Base
from core.models.mixins.id_int_pk import IdIntPkMixin
from core.models.mixins.time_stamp import TimeStampMixin

if TYPE_CHECKING:
    from core.models import User
    from core.models import Task
    from core.models import Meeting


class Team(
    Base,
    IdIntPkMixin,
    TimeStampMixin,
):
    name: Mapped[str] = mapped_column(String(50), unique=True)
    description: Mapped[str | None] = mapped_column(Text, default=None)
    code: Mapped[str] = mapped_column(String, unique=True)

    admin_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    users: Mapped[list["User"]] = relationship(
        back_populates="team",
        passive_deletes=True,
    )

    tasks: Mapped[list["Task"]] = relationship(
        back_populates="team",
        passive_deletes=True,
    )

    meetings: Mapped[list["Meeting"]] = relationship(
        back_populates="team",
        passive_deletes=True,
    )
