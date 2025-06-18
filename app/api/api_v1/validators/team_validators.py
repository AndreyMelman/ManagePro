from fastapi import HTTPException, status

from core.models import User, Team
from core.schemas.user import UpdateRoleRequest
from core.types.role import UserRole


def validate_team_access(
    user: User,
    team: Team,
) -> None:
    if user.team_id != team.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"message": "У вас нет доступа к этой команде"},
        )


def check_team_admin(
    user: User,
    team: Team,
) -> None:
    if team.admin_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "message": f"Только админ команды {team.name} может выполнять это действие"
            },
        )


def ensure_user_is_admin(
    user: User,
) -> None:
    if user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "message": f"Только админ без команды может выполнять это действие"
            },
        )


def disallow_admin_assignment(
    role_data: UpdateRoleRequest,
) -> None:
    if role_data.role == "admin":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "message": "Администратор может назначать только менеджера и сотрудника"
            },
        )


def remove_team_admin(
    user: User,
    team: Team,
) -> None:
    if user.id == team.admin_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": "Нельзя удалить админа команды"},
        )
