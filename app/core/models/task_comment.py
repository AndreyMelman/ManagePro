from typing import TYPE_CHECKING

from sqlalchemy import (
    ForeignKey,
    Integer,
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
    from core.models import Task
    from core.models import User


class TaskComment(
    Base,
    IdIntPkMixin,
    TimeStampMixin,
):
    content: Mapped[str] = mapped_column(Text)

    task_id: Mapped[int] = mapped_column(Integer, ForeignKey("tasks.id"))
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))

    task: Mapped["Task"] = relationship(back_populates="comments")
    user: Mapped["User"] = relationship(back_populates="user_comments")
