from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    String,
    Text,
    DateTime,
    Integer,
    ForeignKey,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from core.models import Base
from core.models.mixins.id_int_pk import IdIntPkMixin
from core.models.mixins.time_stamp import TimeStampMixin
from core.schemas.task import TaskStatus

if TYPE_CHECKING:
    from core.models import TaskComment
    from core.models import User
    from core.models import Team
    from core.models import Evaluation


class Task(
    Base,
    IdIntPkMixin,
    TimeStampMixin,
):
    title: Mapped[str] = mapped_column(String(250))
    description: Mapped[str] = mapped_column(Text, nullable=True)
    deadline: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    status: Mapped[TaskStatus] = mapped_column(String, default=TaskStatus.OPEN)

    creator_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    assignee_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id"),
        nullable=True,
    )
    team_id: Mapped[int] = mapped_column(Integer, ForeignKey("teams.id"))

    creator: Mapped["User"] = relationship(
        back_populates="created_tasks",
        foreign_keys=[creator_id],
    )
    assignee: Mapped["User"] = relationship(
        back_populates="assigned_tasks",
        foreign_keys=[assignee_id],
    )
    team: Mapped["Team"] = relationship(back_populates="tasks")
    comments: Mapped[list["TaskComment"]] = relationship(back_populates="task")
    evaluations: Mapped[list["Evaluation"]] = relationship(back_populates="task")
