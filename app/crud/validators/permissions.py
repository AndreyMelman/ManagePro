from core.models import User, Task, Team
from core.schemas.user import UpdateRoleRequest
from core.types.role import UserRole
from exceptions.task_exceptions import TaskNotTeamError, TaskPermissionError
from exceptions.team_exceptions import (
    TeamAccessDeniedError,
    TeamAdminRequiredError,
    TeamAdminError,
    CannotAddTeamAdminError,
    CannotRemoveTeamAdminError,
)
from exceptions.user_exceptions import (
    UserAlreadyInTeamError,
    UserNotInTeamError,
    UserNotFoundError,
    UserCannotChangeRole,
)


def ensure_user_has_team(
    user: User,
) -> None:
    if not user.team_id:
        raise TaskNotTeamError()


def check_task_owner(
    user: User,
    task: Task,
) -> None:
    if task.creator_id != user.id:
        raise TaskPermissionError()


def validate_team_access(
    user: User,
    team: Team,
) -> None:
    if user.team_id != team.id:
        raise TeamAccessDeniedError()


def ensure_user_in_team(
    user: User,
    team: Team,
) -> None:
    if user.team_id != team.id:
        raise UserNotInTeamError()


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


def ensure_user_not_in_team(
    user: User,
) -> None:
    if user.team_id:
        raise UserAlreadyInTeamError(user.team_id)


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


def ensure_user_exists(
    user: User | None,
) -> None:
    if not user:
        raise UserNotFoundError()


def disallow_self_role_change(
    user: User | None,
    current_user: User,
) -> None:
    if user.id == current_user.id:
        raise UserCannotChangeRole()
