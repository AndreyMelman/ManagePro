from typing import Annotated

from fastapi import APIRouter, Path, Depends

from api.dependencies.load_by_id import task_by_id
from api.dependencies.params import (
    TaskServiceDep,
    CurrentActiveManager,
)
from core.models import Task
from core.schemas.task import (
    TaskSchema,
    TaskCreateShema,
    TaskUpdateShema,
)
from api.docs.teams import (
    TASK_TAG,
)
from exceptions.task_exceptions import TaskPermissionError

router = APIRouter(tags=[TASK_TAG])


@router.get("/{task_id}", response_model=TaskSchema)
async def get_task(
    task: Task = Depends(task_by_id),
):
    return task


@router.post("", response_model=TaskSchema)
async def create_task(
    crud: TaskServiceDep,
    current_user: CurrentActiveManager,
    task_in: TaskCreateShema,
):
    return await crud.create_task(
        current_user=current_user,
        task_in=task_in,
    )


@router.patch("/{task_id}", response_model=TaskSchema)
async def update_task(
    crud: TaskServiceDep,
    current_user: CurrentActiveManager,
    task_update: TaskUpdateShema,
    task: Task = Depends(task_by_id),
):
    return await crud.update_task(
        current_user=current_user,
        task=task,
        task_update=task_update,
        partial=True,
    )
