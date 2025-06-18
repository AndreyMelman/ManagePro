from fastapi import HTTPException, status

from core.models import User, Team


def ensure_user_exists(
    user: User | None,
) -> None:
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": "Пользователь не найден"},
        )


def ensure_user_in_team(
    user: User,
    team: Team,
) -> None:
    if user.team_id != team.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": "Пользователь не состоит в этой команде"},
        )


def ensure_user_not_in_team(
    user: User,
) -> None:
    if user.team_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": f"У пользователя {user.id} уже есть команда"},
        )


def disallow_self_role_change(
    user: User | None,
    current_user: User,
) -> None:
    if user.id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": "Суперпользователь не может изменить свою роль"},
        )
