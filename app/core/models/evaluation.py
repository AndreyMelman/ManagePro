from typing import TYPE_CHECKING

from sqlalchemy import (
    ForeignKey,
    Integer,
    String,
    CheckConstraint,
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


class Evaluation(
    Base,
    IdIntPkMixin,
    TimeStampMixin,
):
    score: Mapped[int] = mapped_column(
        Integer,
        CheckConstraint("score >= 1 AND score <= 5", name="check_score_positive"),
    )
    comment: Mapped[str | None] = mapped_column(String, default=None)

    task_id: Mapped[int] = mapped_column(ForeignKey("tasks.id"))
    evaluator_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    task: Mapped["Task"] = relationship(back_populates="evaluations")
    evaluator: Mapped["User"] = relationship(
        back_populates="evaluations_given",
        foreign_keys=[evaluator_id],
    )
    user: Mapped["User"] = relationship(
        back_populates="evaluations_received",
        foreign_keys=[user_id],
    )
