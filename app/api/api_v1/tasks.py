from fastapi import APIRouter, Depends

from api.dependencies.load_by_id import get_task_by_id
from api.dependencies.params import (
    TaskServiceDep,
    CurrentActiveUser,
)
from core.models import Task
from core.schemas.task import (
    TaskSchema,
    TaskCreateShema,
    TaskUpdateShema,
)
from api.docs.tasks import (
    TASK_TAG,
    GET_TASK,
    CREATE_TASK,
    UPDATE_TASK,
    DELETE_TASK,
)

router = APIRouter(tags=[TASK_TAG])


@router.get(
    "/{task_id}",
    **GET_TASK,
)
async def get_task(
    task: Task = Depends(get_task_by_id),
):
    """
    Получить задачу по ID.

    Args:
        task: Задача

    Returns:
        TaskSchema: Одна задача
    """
    return task


@router.post(
    "",
    **CREATE_TASK,
)
async def create_task(
    crud: TaskServiceDep,
    user: CurrentActiveUser,
    task_in: TaskCreateShema,
):
    """
    Создать новую задачу.

    Args:
        crud: Сервис для работы с задачами
        user: Текущий пользователь
        task_in: Данные для создания задачи

    Returns:
        TaskSchema: Созданная задача
    """
    return await crud.create_task(
        user=user,
        task_in=task_in,
    )


@router.patch(
    "/{task_id}",
    **UPDATE_TASK,
)
async def update_task(
    crud: TaskServiceDep,
    user: CurrentActiveUser,
    task_update: TaskUpdateShema,
    task: Task = Depends(get_task_by_id),
):
    """
    Обновить существующую задачу.

    Args:
        crud: Сервис для работы с задачами
        user: Текущий пользователь
        task_update: Данные для обновления задачи
        task: Задача для обновления

    Returns:
        TaskSchema: Обновленная задача
    """
    return await crud.update_task(
        user=user,
        task=task,
        task_update=task_update,
        partial=True,
    )


@router.delete(
    "/{task_id}",
    **DELETE_TASK,
)
async def delete_task(
    crud: TaskServiceDep,
    user: CurrentActiveUser,
    task: Task = Depends(get_task_by_id),
):
    """
    Удалить задачу.

    Args:
        crud: Сервис для работы с задачами
        user: Текущий пользователь
        task: Задача для удаления

    Returns:
        TaskSchema: Удаленная задача
    """
    return await crud.delete_task(
        task=task,
        user=user,
    )
