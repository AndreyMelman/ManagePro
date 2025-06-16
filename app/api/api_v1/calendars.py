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
from crud.validators.task_validators import ensure_user_has_team

router = APIRouter(tags=["Calendar"])


@router.get("/month", response_model=CalendarMonthView)
async def get_month_view(
    crud: CalendarServiceDep,
    year: Annotated[int, Query(ge=2000, le=2100)],
    month: Annotated[int, Query(ge=1, le=12)],
    user: CurrentActiveUser,
):
    ensure_user_has_team(user)
    return await crud.get_month_view(
        year=year,
        month=month,
        team_id=user.team_id,
    )


@router.get("/day", response_model=CalendarDayView)
async def get_day_view(
    crud: CalendarServiceDep,
    day_date: date,
    user: CurrentActiveUser,
):
    ensure_user_has_team(user)

    return await crud.get_day_view(
        day_date=day_date,
        team_id=user.team_id,
    )
