from fastapi import (
    APIRouter,
    Request,
    Depends,
)

from core.models import User
from utils.templates import templates
from api.dependencies.params import CalendarServiceDep
from app.views.auth.views import get_current_user_from_cookie
from datetime import date, datetime

router = APIRouter()


@router.get("/calendar")
async def calendar_current_month(
    request: Request,
    calendar_service: CalendarServiceDep,
    user: User = Depends(get_current_user_from_cookie),
):
    today = date.today()
    if not user.team_id:
        return templates.TemplateResponse(
            "calendars/month.html",
            {
                "request": request,
                "user": user,
                "month_view": None,
                "year": today.year,
                "month": today.month,
            },
        )
    month_view = await calendar_service.get_month_view(
        year=today.year,
        month=today.month,
        team_id=user.team_id,
    )
    return templates.TemplateResponse(
        "calendars/month.html",
        {
            "request": request,
            "user": user,
            "month_view": month_view,
            "year": today.year,
            "month": today.month,
        },
    )


@router.get("/calendar/day/{day_date}")
async def calendar_day(
    request: Request,
    day_date: str,
    calendar_service: CalendarServiceDep,
    user: User = Depends(get_current_user_from_cookie),
):
    if not user.team_id:
        return templates.TemplateResponse(
            "calendars/day.html",
            {
                "request": request,
                "user": user,
                "day_view": None,
                "day_date": day_date,
            },
        )
    day = datetime.strptime(day_date, "%Y-%m-%d").date()
    day_view = await calendar_service.get_day_view(
        day_date=day,
        team_id=user.team_id,
    )
    return templates.TemplateResponse(
        "calendars/day.html",
        {
            "request": request,
            "user": user,
            "day_view": day_view,
            "day_date": day_date,
        },
    )


@router.get("/calendar/{year}/{month}")
async def calendar_month(
    request: Request,
    year: int,
    month: int,
    calendar_service: CalendarServiceDep,
    user: User = Depends(get_current_user_from_cookie),
):
    if not user.team_id:
        return templates.TemplateResponse(
            "calendars/month.html",
            {
                "request": request,
                "user": user,
                "month_view": None,
                "year": year,
                "month": month,
            },
        )
    month_view = await calendar_service.get_month_view(
        year=year,
        month=month,
        team_id=user.team_id,
    )
    return templates.TemplateResponse(
        "calendars/month.html",
        {
            "request": request,
            "user": user,
            "month_view": month_view,
            "year": year,
            "month": month,
        },
    )
