from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from core.models import Base

if TYPE_CHECKING:
    from core.models import Meeting
    from core.models import User


class MeetingParticipants(Base):
    meeting_id: Mapped[int] = mapped_column(ForeignKey("meetings.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    meeting: Mapped["Meeting"] = relationship(back_populates="participants")
    user: Mapped["User"] = relationship(back_populates="meetings")
