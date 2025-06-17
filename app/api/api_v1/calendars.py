from datetime import date
from typing import Annotated

from fastapi import (
    APIRouter,
    Query,
)
from api.dependencies.params import (
    CurrentActiveUser,
    CalendarServiceDep,
)
from core.schemas.calendar import (
    CalendarMonthView,
    CalendarDayView,
)
from api.api_v1.validators.task_validators import ensure_user_has_team
from api.docs.calendars import (
    CALENDAR_TAG,
    GET_MONTH_VIEW,
    GET_DAY_VIEW,
)

router = APIRouter(tags=[CALENDAR_TAG])


@router.get("/month", **GET_MONTH_VIEW)
async def get_month_view(
    crud: CalendarServiceDep,
    year: Annotated[int, Query(ge=2000, le=2100)],
    month: Annotated[int, Query(ge=1, le=12)],
    user: CurrentActiveUser,
):
    """
    Получить календарь на месяц.

    Args:
        crud: Сервис для работы с календарем
        year: Год
        month: Месяц
        user: Текущий пользователь

    Returns:
        CalendarMonthView: Календарь на месяц
    """
    ensure_user_has_team(user)
    return await crud.get_month_view(
        year=year,
        month=month,
        team_id=user.team_id,
    )


@router.get("/day", **GET_DAY_VIEW)
async def get_day_view(
    crud: CalendarServiceDep,
    day_date: date,
    user: CurrentActiveUser,
):
    """
    Получить календарь на день.

    Args:
        crud: Сервис для работы с календарем
        day_date: Дата
        user: Текущий пользователь

    Returns:
        CalendarDayView: Календарь на день
    """
    ensure_user_has_team(user)

    return await crud.get_day_view(
        day_date=day_date,
        team_id=user.team_id,
    )
