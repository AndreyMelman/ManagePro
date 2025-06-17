from core.models import User, Team
from core.schemas.user import UpdateRoleRequest
from core.types.role import UserRole

from exceptions.team_exceptions import (
    TeamAccessDeniedError,
    TeamAdminRequiredError,
    TeamAdminError,
    CannotAddTeamAdminError,
    CannotRemoveTeamAdminError,
)


def validate_team_access(
    user: User,
    team: Team,
) -> None:
    if user.team_id != team.id:
        raise TeamAccessDeniedError()


def check_team_admin(
    user: User,
    team: Team,
) -> None:
    if team.admin_id != user.id:
        raise TeamAdminRequiredError(team.name)


def ensure_user_is_admin(
    user: User,
) -> None:
    if user.role != UserRole.ADMIN:
        raise TeamAdminError()


def disallow_admin_assignment(
    role_data: UpdateRoleRequest,
) -> None:
    if role_data.role == "admin":
        raise CannotAddTeamAdminError()


def remove_team_admin(
    user: User,
    team: Team,
) -> None:
    if user.id == team.admin_id:
        raise CannotRemoveTeamAdminError()
