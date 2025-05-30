from fastapi import APIRouter, Depends

from api.dependencies.load_by_id import get_task_by_id
from api.dependencies.params import CurrentActiveUser, TaskCommentServiceDep
from core.models import Task
from core.schemas.task_comment import TaskCommentCreateSchema, TaskCommentSchema

router = APIRouter(tags=["Task Comments"])


@router.post("/{task_id}", response_model=TaskCommentSchema)
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
