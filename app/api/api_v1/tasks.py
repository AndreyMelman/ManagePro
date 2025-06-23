from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

from api.api_v1.validators.task_validators import (
    ensure_user_has_team,
    check_task_owner,
)
from api.dependencies.load_by_id import (
    get_task_by_id,
    get_user_by_id,
)
from api.dependencies.params import (
    TaskServiceDep,
    CurrentActiveUser,
)
from core.models import Task, User
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


@router.get("", response_model=list[TaskSchema])
async def tasks_get(
    crud: TaskServiceDep,
    user: CurrentActiveUser,
):
    return await crud.get_tasks(user=user)


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
    ensure_user_has_team(user)
    if task_in.assignee_id is not None:
        assignee = await get_user_by_id(task_in.assignee_id, crud.session)
        if assignee is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "message": "Исполнитель должен быть из той же команды, что и руководитель."
                },
            )

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
    current_user: CurrentActiveUser,
    task_update: TaskUpdateShema,
    partial: bool = True,
    task: Task = Depends(get_task_by_id),
):
    """
    Обновить существующую задачу.

    Args:
        crud: Сервис для работы с задачами
        current_user: Текущий пользователь
        task_update: Данные для обновления задачи
        task: Задача для обновления
        partial: Флаг частичного обновления

    Returns:
        TaskSchema: Обновленная задача
    """
    check_task_owner(current_user, task)

    update_data = task_update.model_dump(exclude_unset=partial)

    assignee = None
    if "assignee_id" in update_data and update_data["assignee_id"] is not None:
        assignee = await get_user_by_id(update_data["assignee_id"], crud.session)
        if assignee.team_id != current_user.team_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "message": "Исполнитель должен быть из той же команды, что и руководитель."
                },
            )

    updated_task = await crud.update_task(
        task=task,
        update_data=update_data,
        assignee=assignee,
    )
    return updated_task


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
    check_task_owner(user, task)
    return await crud.delete_task(task)
