from fastapi import (
    APIRouter,
    Depends,
)

from api.api_v1.validators.task_validators import (
    check_user_command,
    check_task_comment_owner,
)
from api.dependencies.load_by_id import (
    get_task_by_id,
    get_task_comment_by_id,
)
from api.dependencies.params import (
    CurrentActiveUser,
    TaskCommentServiceDep,
)
from core.models import (
    Task,
    TaskComment,
)
from core.schemas.task_comment import (
    TaskCommentCreateSchema,
    TaskCommentSchema,
    TaskCommentUpdateSchema,
)
from api.docs.task_comments import (
    TASK_COMMENT_TAG,
    GET_TASK_COMMENTS,
    CREATE_TASK_COMMENT,
    UPDATE_TASK_COMMENT,
    DELETE_TASK_COMMENT,
)

router = APIRouter(tags=[TASK_COMMENT_TAG])


@router.get(
    "/{task_id}",
    **GET_TASK_COMMENTS,
)
async def get_task_comments(
    crud: TaskCommentServiceDep,
    user: CurrentActiveUser,
    task: Task = Depends(get_task_by_id),
):
    """
    Получить комментарии к задаче.

    Args:
        crud: Сервис для работы с комментариями
        user: Текущий пользователь
        task: Задача

    Returns:
        list[TaskCommentSchema]: Список комментариев
    """
    check_user_command(user, task)

    return await crud.get_task_comments(task)


@router.post(
    "/{task_id}",
    **CREATE_TASK_COMMENT,
)
async def create_task_comment(
    crud: TaskCommentServiceDep,
    user: CurrentActiveUser,
    comment_in: TaskCommentCreateSchema,
    task: Task = Depends(get_task_by_id),
):
    """
    Создать комментарий к задаче.

    Args:
        crud: Сервис для работы с комментариями
        user: Текущий пользователь
        comment_in: Данные для создания комментария
        task: Задача

    Returns:
        TaskCommentSchema: Созданный комментарий
    """
    check_user_command(user, task)

    return await crud.create_task_comment(
        task=task,
        user=user,
        comment_in=comment_in,
    )


@router.put(
    "/{task_id}",
    **UPDATE_TASK_COMMENT,
)
async def update_task_comment(
    crud: TaskCommentServiceDep,
    user: CurrentActiveUser,
    comment_update: TaskCommentUpdateSchema,
    comment: TaskComment = Depends(get_task_comment_by_id),
):
    """
    Обновить комментарий.

    Args:
        crud: Сервис для работы с комментариями
        user: Текущий пользователь
        comment_update: Данные для обновления комментария
        comment: Комментарий для обновления

    Returns:
        TaskCommentSchema: Обновленный комментарий
    """
    check_task_comment_owner(user, comment)

    return await crud.update_task_comment(
        comment=comment,
        comment_update=comment_update,
    )


@router.delete(
    "/{task_id}",
    **DELETE_TASK_COMMENT,
)
async def delete_task_comment(
    crud: TaskCommentServiceDep,
    user: CurrentActiveUser,
    comment: TaskComment = Depends(get_task_comment_by_id),
):
    """
    Удалить комментарий.

    Args:
        crud: Сервис для работы с комментариями
        user: Текущий пользователь
        comment: Комментарий для удаления

    Returns:
        None
    """
    check_task_comment_owner(user, comment)

    return await crud.delete_task_comment(comment)
