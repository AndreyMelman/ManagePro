from fastapi import HTTPException, status

from core.models import Task
from core.schemas.task import TaskStatus
from exceptions.evaluation_exceptions import (
    DuplicateEstimateError,
)


def already_estimated(
    existing_evaluation,
) -> None:
    if existing_evaluation.scalar_one_or_none():
        raise DuplicateEstimateError()


def is_task_completed(
    task: Task,
) -> None:
    if task.status != TaskStatus.COMPLETED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": "Нельзя ставить оценку задаче, которая не выполнена"},
        )
