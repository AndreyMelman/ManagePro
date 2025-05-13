from fastapi import APIRouter, status

from api.dependencies.params import (
    TeamServiceDep,
    CurrentActiveAdmin,
    CurrentActiveUser,
)
from core.schemas.team import TeamCreateSchema, TeamSchema

from api.docs.teams import (
    TEAM_TAG,
    GET_TEAM_WITH_USERS,
    CREATE_TEAM,
    ADD_USER_TO_TEAM,
    REMOVE_USER_FROM_TEAM,
    UPDATE_ROLE_FROM_USER,
)
from core.schemas.user import UpdateRoleRequest

router = APIRouter(tags=[TEAM_TAG])


@router.get(
    "/",
    **GET_TEAM_WITH_USERS,
)
async def get_team_with_users(
    crud: TeamServiceDep,
    user: CurrentActiveAdmin,
    team_id: int,
):
    """
    Получить состав команды.

    Args:
        crud: Сервис для работы с командами
        user: Текущий пользователь
        team_id: ID команды

    Returns:
        list[TeamSchema]: Список с одной командой и её пользователями
    """
    return await crud.get_team_with_users(
        team_id=team_id,
        current_user=user,
    )


@router.post(
    "",
    **CREATE_TEAM,
)
async def create_team(
    crud: TeamServiceDep,
    user: CurrentActiveAdmin,
    team_in: TeamCreateSchema,
):
    """
    Создать новую команду.

    Args:
        crud: Сервис для работы с командами
        user: Текущий пользователь
        team_in: Данные для создания команды

    Returns:
        TeamSchema: Созданная команда
    """
    return await crud.create_team(
        user=user,
        team_in=team_in,
    )


@router.post("/{team_id}/user/{user_id}", **ADD_USER_TO_TEAM)
async def add_user_to_team(
    crud: TeamServiceDep,
    user: CurrentActiveAdmin,
    team_id: int,
    user_id: int,
):
    """
    Добавить пользователя в команду.

    Args:
        crud: Сервис для работы с командами
        user: Текущий пользователь
        team_id: ID команды
        user_id: ID пользователя
    """
    return await crud.add_user_to_team(
        current_user=user,
        team_id=team_id,
        user_id=user_id,
    )


@router.patch(
    "/{team_id}/user/{user_id}/role",
    **UPDATE_ROLE_FROM_USER,
)
async def update_user_team_role(
    crud: TeamServiceDep,
    user: CurrentActiveAdmin,
    role_data: UpdateRoleRequest,
    team_id: int,
    user_id: int,
):
    """
    Добавить роль пользователю в команде.

    Args:
        crud: Сервис для работы с командами
        user: Текущий пользователь
        role_data: Данные для обновления роли
        team_id: ID команды
        user_id: ID пользователя
    """
    return await crud.update_user_team_role(
        team_id=team_id,
        user_id=user_id,
        current_user=user,
        role_data=role_data,
    )


@router.delete(
    "/{team_id}/user/{user_id}",
    **REMOVE_USER_FROM_TEAM,
)
async def remove_user_from_team(
    crud: TeamServiceDep,
    user: CurrentActiveAdmin,
    team_id: int,
    user_id: int,
):
    """
    Удалить пользователя из команды.

    Args:
        crud: Сервис для работы с командами
        user: Текущий пользователь
        team_id: ID команды
        user_id: ID пользователя
    """
    return await crud.remove_user_from_team(
        current_user=user,
        team_id=team_id,
        user_id=user_id,
    )
