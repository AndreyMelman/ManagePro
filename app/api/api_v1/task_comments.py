from fastapi import APIRouter, Depends

from api.dependencies.load_by_id import get_task_by_id, get_task_comment_by_id
from api.dependencies.params import CurrentActiveUser, TaskCommentServiceDep
from core.models import Task, TaskComment
from core.schemas.task_comment import (
    TaskCommentCreateSchema,
    TaskCommentSchema,
    TaskCommentUpdateSchema,
)

router = APIRouter(tags=["Task Comments"])


@router.get(
    "/{task_id}",
    response_model=list[TaskCommentSchema],
)
async def get_task_comments(
    crud: TaskCommentServiceDep,
    current_user: CurrentActiveUser,
    task: Task = Depends(get_task_by_id),
):
    return await crud.get_task_comments(
        task=task,
        current_user=current_user,
    )


@router.post(
    "/{task_id}",
    response_model=TaskCommentSchema,
)
async def create_task_comment(
    crud: TaskCommentServiceDep,
    current_user: CurrentActiveUser,
    comment_in: TaskCommentCreateSchema,
    task: Task = Depends(get_task_by_id),
):
    return await crud.create_task_comment(
        task=task,
        current_user=current_user,
        comment_in=comment_in,
    )


@router.put(
    "/{task_id}",
    response_model=TaskCommentSchema,
)
async def update_task_comment(
    crud: TaskCommentServiceDep,
    current_user: CurrentActiveUser,
    comment_update: TaskCommentUpdateSchema,
    comment: TaskComment = Depends(get_task_comment_by_id),
):
    return await crud.update_task_comment(
        comment=comment,
        current_user=current_user,
        comment_update=comment_update,
    )


@router.delete("/{task_id}")
async def delete_task_comment(
    crud: TaskCommentServiceDep,
    current_user: CurrentActiveUser,
    comment: TaskComment = Depends(get_task_comment_by_id),
):
    return await crud.delete_task_comment(
        comment=comment,
        current_user=current_user,
    )
