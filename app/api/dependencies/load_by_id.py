from typing import Annotated

from fastapi import Path

from api.dependencies.params import TaskServiceDep, CurrentActiveManager
from core.models import Task
from exceptions.task_exceptions import TaskNotFoundError


async def task_by_id(
    task_id: Annotated[int, Path()],
    crud: TaskServiceDep,
    current_user: CurrentActiveManager,
) -> Task:
    task = await crud.get_task(
        current_user=current_user,
        task_id=task_id,
    )
    if task is not None:
        return task
    raise TaskNotFoundError()
