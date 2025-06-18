from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.params import Query

from api.api_v1.validators.evaluation_validators import is_task_completed
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
from api.docs.evaluations import (
    EVALUATION_TAG,
    GET_EVALUATIONS,
    GET_AVERAGE_SCORE,
    CREATE_EVALUATION,
)

router = APIRouter(tags=[EVALUATION_TAG])


@router.get("", **GET_EVALUATIONS)
async def get_evaluations(
    crud: EvaluationServiceDep,
    user: CurrentActiveUser,
):
    """
    Получить оценки пользователя.

    Args:
        crud: Сервис для работы с оценками
        user: Текущий пользователь

    Returns:
        list[EvaluationBaseSchema]: Список оценок
    """
    return await crud.get_evaluations(user)


@router.get("/average", **GET_AVERAGE_SCORE)
async def get_average_score(
    crud: EvaluationServiceDep,
    user: CurrentActiveUser,
    start_date: Annotated[datetime | None, Query()] = None,
    end_date: Annotated[datetime | None, Query()] = None,
):
    """
    Получить среднюю оценку.

    Args:
        crud: Сервис для работы с оценками
        user: Текущий пользователь
        start_date: Начальная дата периода
        end_date: Конечная дата периода

    Returns:
        dict: Средняя оценка и статистика
    """
    return await crud.get_average_score(
        user=user,
        start_date=start_date,
        end_date=end_date,
    )


@router.post(
    "/{task_id}",
    **CREATE_EVALUATION,
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
        user: Текущий пользователь
        evaluation_in: Данные для создания оценки
        task: Задача

    Returns:
        EvaluationSchema: Созданная оценка
    """
    is_task_completed(task)

    return await crud.create_evaluation(
        evaluation_in=evaluation_in,
        user=user,
        task=task,
    )
