from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.params import Query
from sqlalchemy.testing.suite.test_reflection import users

from api.dependencies.load_by_id import get_task_by_id
from api.dependencies.params import (
    EvaluationServiceDep,
    CurrentActiveUser,
)
from core.models import Task
from core.schemas.evaluation import (
    EvaluationSchema,
    EvaluationCreateSchema,
    EvaluationBaseSchema,
)

router = APIRouter(tags=["Evaluations"])


@router.get("", response_model=list[EvaluationBaseSchema])
async def get_evaluations(
    crud: EvaluationServiceDep,
    user: CurrentActiveUser,
):
    return await crud.get_evaluations(user)


@router.get("/average")
async def get_average_score(
    crud: EvaluationServiceDep,
    user: CurrentActiveUser,
    start_date: Annotated[datetime | None, Query()] = None,
    end_date: Annotated[datetime | None, Query()] = None,
):
    return await crud.get_average_score(
        user=user,
        start_date=start_date,
        end_date=end_date,
    )


@router.post(
    "/{task_id}",
    response_model=EvaluationSchema,
)
async def create_evaluation(
    crud: EvaluationServiceDep,
    user: CurrentActiveUser,
    evaluation_in: EvaluationCreateSchema,
    task: Task = Depends(get_task_by_id),
):
    """
    Создать новую оценку.

    Args:
        crud: Сервис для работы с оценками
        user: Текущий администратор
        evaluation_in: Данные для создания оценки
        task

    Returns:
        EvaluationSchema: Созданная оценка
    """
    return await crud.create_evaluation(
        evaluation_in=evaluation_in,
        user=user,
        task=task,
    )
