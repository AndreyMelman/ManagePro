from fastapi import (
    APIRouter,
    Request,
    Form,
    Depends,
    status,
    HTTPException,
)
from fastapi.responses import RedirectResponse
from api.dependencies.params import (
    TaskCommentServiceDep,
    TaskServiceDep,
)
from app.views.auth.views import get_current_user_from_cookie
from core.models import User
from core.schemas.task_comment import TaskCommentCreateSchema

router = APIRouter()


@router.post("/tasks/{task_id}/comments/add")
async def add_comment(
    request: Request,
    task_id: int,
    comment_service: TaskCommentServiceDep,
    task_service: TaskServiceDep,
    user: User = Depends(get_current_user_from_cookie),
    content: str = Form(...),
):
    task = await task_service.get_task(user, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    comment_in = TaskCommentCreateSchema(content=content)
    await comment_service.create_task_comment(task, user, comment_in)
    return RedirectResponse(url=f"/tasks/{task_id}", status_code=status.HTTP_302_FOUND)


@router.post("/tasks/{task_id}/comments/{comment_id}/delete")
async def delete_comment(
    task_id: int,
    comment_id: int,
    comment_service: TaskCommentServiceDep,
    task_service: TaskServiceDep,
    user: User = Depends(get_current_user_from_cookie),
):
    task = await task_service.get_task(user, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    comment = await comment_service.get_task_comment(task, comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Комментарий не найден")
    await comment_service.delete_task_comment(comment)
    return RedirectResponse(url=f"/tasks/{task_id}", status_code=status.HTTP_302_FOUND)
