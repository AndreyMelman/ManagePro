from fastapi import (
    APIRouter,
    Request,
    Form,
    Depends,
    status,
    HTTPException,
)
from fastapi.responses import RedirectResponse
from utils.templates import templates
from api.dependencies.params import (
    EvaluationServiceDep,
    TaskServiceDep,
)
from app.views.auth.views import get_current_user_from_cookie
from core.schemas.evaluation import EvaluationCreateSchema
from core.models import User

router = APIRouter()


@router.get("/evaluations")
async def evaluations_list(
    request: Request,
    evaluation_service: EvaluationServiceDep,
    user: User = Depends(get_current_user_from_cookie),
):
    evaluations = await evaluation_service.get_evaluations(user)
    return templates.TemplateResponse(
        "evaluations/list.html",
        {"request": request, "user": user, "evaluations": evaluations},
    )


@router.get("/evaluations/give/{task_id}")
async def give_evaluation_get(
    request: Request,
    task_id: int,
    task_service: TaskServiceDep,
    user: User = Depends(get_current_user_from_cookie),
):
    task = await task_service.get_task(user, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Задача не найдена")

    if user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Нет прав для выставления оценки",
        )
    return templates.TemplateResponse(
        "evaluations/give.html",
        {
            "request": request,
            "user": user,
            "task": task,
        },
    )


@router.post("/evaluations/give/{task_id}")
async def give_evaluation_post(
    request: Request,
    task_id: int,
    evaluation_service: EvaluationServiceDep,
    task_service: TaskServiceDep,
    user: User = Depends(get_current_user_from_cookie),
    score: int = Form(...),
    comment: str = Form(None),
):
    task = await task_service.get_task(user, task_id)
    if not task:
        raise HTTPException(
            status_code=404,
            detail="Задача не найдена",
        )
    if user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Нет прав для выставления оценки",
        )
    evaluation_in = EvaluationCreateSchema(score=score, comment=comment)
    await evaluation_service.create_evaluation(evaluation_in, user, task)
    return RedirectResponse(
        url="/evaluations",
        status_code=status.HTTP_302_FOUND,
    )
