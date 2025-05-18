from core.models import User, Team

from exceptions.user_exceptions import (
    UserAlreadyInTeamError,
    UserNotInTeamError,
    UserNotFoundError,
    UserCannotChangeRole,
)


def ensure_user_exists(
    user: User | None,
) -> None:
    if not user:
        raise UserNotFoundError()


def ensure_user_in_team(
    user: User,
    team: Team,
) -> None:
    if user.team_id != team.id:
        raise UserNotInTeamError()


def ensure_user_not_in_team(
    user: User,
) -> None:
    if user.team_id:
        raise UserAlreadyInTeamError(user.team_id)


def disallow_self_role_change(
    user: User | None,
    current_user: User,
) -> None:
    if user.id == current_user.id:
        raise UserCannotChangeRole()
