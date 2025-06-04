from core.models import Task
from core.schemas.task import TaskStatus
from exceptions.evaluation_exceptions import (DuplicateEstimateError, TaskNotCompletedError,)


def already_estimated(
    existing_evaluation,
) -> None:
    if existing_evaluation.scalar_one_or_none():
        raise DuplicateEstimateError()


def is_task_completed(
    task: Task,
) -> None:
    if task.status != TaskStatus.COMPLETED:
        raise TaskNotCompletedError()