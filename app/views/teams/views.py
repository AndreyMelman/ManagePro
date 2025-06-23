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
    TeamServiceDep,
    UserServiceDep,
)
from app.views.auth.views import get_current_user_from_cookie
from core.schemas.team import TeamCreateSchema

router = APIRouter()


@router.get("/team")
async def team_get(
    request: Request,
    team_service: TeamServiceDep,
    user: User = Depends(get_current_user_from_cookie),
):
    if not getattr(user, "team_id", None):
        if user.role == "admin":
            return templates.TemplateResponse(
                "teams/team.html",
                {
                    "request": request,
                    "user": user,
                    "show_create": True,
                },
            )
        else:
            return templates.TemplateResponse(
                "teams/team.html",
                {
                    "request": request,
                    "user": user,
                    "show_none": True,
                },
            )

    team = await team_service.get_team(user.team_id, user)
    team_info = team
    is_admin = user.id == getattr(team, "admin_id", None)
    users = team.users if team else []
    return templates.TemplateResponse(
        "teams/team.html",
        {
            "request": request,
            "user": user,
            "team": team,
            "team_info": team_info,
            "is_admin": is_admin,
            "users": users,
        },
    )


@router.post("/team/create")
async def team_create_post(
    team_service: TeamServiceDep,
    name: str = Form(...),
    description: str = Form(None),
    code: str = Form(...),
    user: User = Depends(get_current_user_from_cookie),
):
    if not (user.role == "admin" and not getattr(user, "team_id", None)):
        raise HTTPException(status_code=403, detail="Нет прав")
    team_in = TeamCreateSchema(
        name=name,
        description=description,
        code=code,
    )
    await team_service.create_team(
        team_in=team_in,
        user=user,
    )
    return RedirectResponse(url="/team", status_code=status.HTTP_302_FOUND)


@router.post("/team/add_user")
async def add_user_to_team(
    request: Request,
    team_service: TeamServiceDep,
    user_service: UserServiceDep,
    email: str = Form(...),
    user: User = Depends(get_current_user_from_cookie),
):
    user_to_add = await user_service.get_user_by_email(email)
    if user_to_add is None:
        return templates.TemplateResponse(
            "teams/team.html",
            {
                "request": request,
                "user": user,
                "error": "Пользователь не найден",
            },
            status_code=400,
        )
    team = await team_service.get_team(user.team_id, user)
    await team_service.add_user_to_team(team, user_to_add)
    return RedirectResponse(url="/team", status_code=status.HTTP_302_FOUND)


@router.post("/team/remove_user")
async def remove_user_from_team(
    request: Request,
    team_service: TeamServiceDep,
    user_service: UserServiceDep,
    user_id: int = Form(...),
    user: User = Depends(get_current_user_from_cookie),
):
    user_to_remove = await user_service.get_user_by_id(user_id)
    if user_to_remove is None:
        return templates.TemplateResponse(
            "teams/team.html",
            {
                "request": request,
                "user": user,
                "error": "Пользователь не найден",
            },
            status_code=400,
        )
    await team_service.remove_user_from_team(user_to_remove)
    return RedirectResponse(url="/team", status_code=status.HTTP_302_FOUND)


@router.post("/team/change_role")
async def change_user_role(
    request: Request,
    team_service: TeamServiceDep,
    user_service: UserServiceDep,
    user_id: int = Form(...),
    role: str = Form(...),
    user: User = Depends(get_current_user_from_cookie),
):
    user_to_update = await user_service.get_user_by_id(user_id)
    if user_to_update is None:
        return templates.TemplateResponse(
            "teams/team.html",
            {
                "request": request,
                "user": user,
                "error": "Пользователь не найден",
            },
            status_code=400,
        )
    from core.schemas.user import UpdateRoleRequest

    await team_service.update_user_team_role(
        user_to_update, UpdateRoleRequest(role=role)
    )
    return RedirectResponse(url="/team", status_code=status.HTTP_302_FOUND)
