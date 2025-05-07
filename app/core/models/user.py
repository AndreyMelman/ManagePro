from typing import TYPE_CHECKING

from fastapi_users_db_sqlalchemy import (
    SQLAlchemyBaseUserTable,
    SQLAlchemyUserDatabase,
)
from sqlalchemy import (
    String,
    ForeignKey,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from core.types.user_id import UserIdType
from core.types.role import UserRole
from .base import Base
from .mixins.id_int_pk import IdIntPkMixin
from .mixins.time_stamp import TimeStampMixin

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession
    from core.models import Team
    from core.models import Task
    from core.models import TaskComment
    from core.models import Evaluation
    from core.models import Meeting


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

    team_id: Mapped[int] = mapped_column(
        ForeignKey("teams.id", ondelete="SET NULL"),
        nullable=True,
    )

    team: Mapped["Team"] = relationship(back_populates="users")
    user_comments: Mapped[list["TaskComment"]] = relationship(back_populates="user")
    created_tasks: Mapped[list["Task"]] = relationship(
        back_populates="creator",
        foreign_keys="Task.creator_id",
    )
    assigned_tasks: Mapped[list["Task"]] = relationship(
        back_populates="assignee",
        foreign_keys="Task.assignee_id",
    )
    evaluations_given: Mapped[list["Evaluation"]] = relationship(
        back_populates="evaluator",
        foreign_keys="Evaluation.evaluator_id",
    )
    evaluations_received: Mapped[list["Evaluation"]] = relationship(
        back_populates="user",
        foreign_keys="Evaluation.user_id",
    )
    organized_meetings: Mapped[list["Meeting"]] = relationship(
        back_populates="organizer",
    )
    meetings: Mapped[list["Meeting"]] = relationship(
        secondary="meeting_participants",
        back_populates="participants",
    )

    @classmethod
    def get_db(cls, session: "AsyncSession"):
        return SQLAlchemyUserDatabase(session, cls)
