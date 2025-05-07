from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    String,
    DateTime,
    Boolean,
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
    from core.models import Team
    from core.models import User


class Meeting(
    Base,
    IdIntPkMixin,
    TimeStampMixin,
):
    title: Mapped[str] = mapped_column(String)
    description: Mapped[str | None] = mapped_column(Text, default=None)
    start_datetime: Mapped[datetime] = mapped_column(DateTime)
    end_datetime: Mapped[datetime] = mapped_column(DateTime)
    is_cancelled: Mapped[bool] = mapped_column(Boolean, default=False)

    organizer_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"))

    organizer: Mapped["User"] = relationship(back_populates="organized_meetings")
    team: Mapped["Team"] = relationship(back_populates="meetings")
    participants: Mapped[list["User"]] = relationship(
        secondary="meeting_participants",
        back_populates="meetings",
    )
