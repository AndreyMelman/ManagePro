from datetime import datetime

from fastapi import (
    APIRouter,
    Request,
    Form,
    Depends,
    status,
    HTTPException,
)
from fastapi.responses import RedirectResponse

from core.models import User
from utils.templates import templates
from api.dependencies.params import (
    TaskServiceDep,
    TaskCommentServiceDep,
)
from app.views.auth.views import get_current_user_from_cookie
from core.schemas.task import TaskCreateShema

router = APIRouter()


@router.get("/tasks")
async def tasks_list(
    request: Request,
    task_service: TaskServiceDep,
    user: User = Depends(get_current_user_from_cookie),
):
    tasks = await task_service.get_tasks(user)
    return templates.TemplateResponse(
        "tasks/list.html", {"request": request, "user": user, "tasks": tasks}
    )


@router.get("/tasks/create")
async def task_create_get(
    request: Request,
    user: User = Depends(get_current_user_from_cookie),
):
    return templates.TemplateResponse(
        "tasks/create.html",
        {"request": request, "user": user},
    )


@router.post("/tasks/create")
async def task_create_post(
    task_service: TaskServiceDep,
    user: User = Depends(get_current_user_from_cookie),
    title: str = Form(...),
    description: str = Form(...),
    deadline: datetime = Form(...),
):
    task_in = TaskCreateShema(
        title=title,
        description=description,
        deadline=deadline,
    )
    await task_service.create_task(user, task_in)
    return RedirectResponse(url="/tasks", status_code=status.HTTP_302_FOUND)


@router.get("/tasks/{task_id}")
async def task_detail(
    request: Request,
    task_id: int,
    task_service: TaskServiceDep,
    comment_service: TaskCommentServiceDep,
    user: User = Depends(get_current_user_from_cookie),
):
    task = await task_service.get_task(user, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    comments = await comment_service.get_task_comments(task)
    return templates.TemplateResponse(
        "tasks/detail.html",
        {"request": request, "user": user, "task": task, "comments": comments},
    )


@router.post("/tasks/{task_id}/delete")
async def task_delete(
    task_id: int,
    task_service: TaskServiceDep,
    user: User = Depends(get_current_user_from_cookie),
):
    task = await task_service.get_task(user, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    await task_service.delete_task(task)
    return RedirectResponse(url="/tasks", status_code=status.HTTP_302_FOUND)
