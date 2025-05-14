from fastapi import APIRouter

from api.dependencies.params import (
    TaskServiceDep,
    CurrentActiveManager,
)
from core.schemas.task import (
    TaskSchema,
    TaskCreateShema,
)
from api.docs.teams import (
    TASK_TAG,
)

router = APIRouter(tags=[TASK_TAG])


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
