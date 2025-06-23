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
    MeetingServiceDep,
    UserServiceDep,
)
from app.views.auth.views import get_current_user_from_cookie
from core.schemas.meeting import MeetingCreateSchema
from core.models import User
from datetime import datetime

router = APIRouter()


@router.get("/meetings")
async def meetings_list(
    request: Request,
    meeting_service: MeetingServiceDep,
    user: User = Depends(get_current_user_from_cookie),
):
    meetings = await meeting_service.get_user_meetings(user)
    return templates.TemplateResponse(
        "meetings/list.html",
        {
            "request": request,
            "user": user,
            "meetings": meetings,
        },
    )


@router.get("/meetings/create")
async def meeting_create_get(
    request: Request,
    user_service: UserServiceDep,
    user: User = Depends(get_current_user_from_cookie),
):
    team_users = []
    if user.team_id:
        from sqlalchemy import select
        from core.models import User as UserModel

        stmt = select(UserModel).where(UserModel.team_id == user.team_id)
        result = await user_service.session.execute(stmt)
        team_users = result.scalars().all()
    return templates.TemplateResponse(
        "meetings/create.html",
        {
            "request": request,
            "user": user,
            "team_users": team_users,
        },
    )


@router.post("/meetings/create")
async def meeting_create_post(
    meeting_service: MeetingServiceDep,
    user: User = Depends(get_current_user_from_cookie),
    title: str = Form(...),
    description: str = Form(...),
    start_datetime: datetime = Form(...),
    end_datetime: datetime = Form(...),
    participants: list[int] = Form(...),
):
    meeting_in = MeetingCreateSchema(
        title=title,
        description=description,
        start_datetime=start_datetime,
        end_datetime=end_datetime,
        participants=participants,
    )
    await meeting_service.create_meeting(
        meeting_in,
        user,
    )
    return RedirectResponse(
        url="/meetings",
        status_code=status.HTTP_302_FOUND,
    )


@router.get("/meetings/{meeting_id}")
async def meeting_detail(
    request: Request,
    meeting_id: int,
    meeting_service: MeetingServiceDep,
    user: User = Depends(get_current_user_from_cookie),
):
    meeting = await meeting_service.get_meeting(meeting_id, user)
    if not meeting:
        raise HTTPException(status_code=404, detail="Встреча не найдена")
    return templates.TemplateResponse(
        "meetings/detail.html",
        {"request": request, "user": user, "meeting": meeting},
    )


@router.post("/meetings/{meeting_id}/cancel")
async def meeting_cancel(
    meeting_id: int,
    meeting_service: MeetingServiceDep,
    user: User = Depends(get_current_user_from_cookie),
):
    meeting = await meeting_service.get_meeting(meeting_id, user)
    if not meeting:
        raise HTTPException(status_code=404, detail="Встреча не найдена")
    await meeting_service.cancel_meeting(meeting)
    return RedirectResponse(url="/meetings", status_code=status.HTTP_302_FOUND)
