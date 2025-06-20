from typing import Annotated
from fastapi import (
    APIRouter,
    Path,
    Query,
    Depends,
)

from api.api_v1.validators.team_validators import (
    check_team_admin,
    disallow_admin_assignment,
    validate_team_access,
    remove_team_admin,
    ensure_user_is_admin,
)
from api.api_v1.validators.user_validators import (
    ensure_user_not_in_team,
    ensure_user_in_team,
)
from api.dependencies.load_by_id import (
    get_team_by_id,
    get_user_by_id,
)
from api.dependencies.params import (
    TeamServiceDep,
    CurrentActiveUser,
)
from core.models import Team
from core.schemas.team import (
    TeamCreateSchema,
    TeamSchema,
)
from api.docs.teams import (
    TEAM_TAG,
    GET_TEAM_WITH_USERS,
    CREATE_TEAM,
    ADD_USER_TO_TEAM,
    REMOVE_USER_FROM_TEAM,
    UPDATE_ROLE_FROM_USER,
    GET_TEAM,
)
from core.schemas.user import UpdateRoleRequest
from core.types.role import UserRole
from core.types.user_id import UserIdType

router = APIRouter(tags=[TEAM_TAG])

TeamID = Annotated[UserIdType, Path()]
UserID = Annotated[UserIdType, Path()]


@router.get(
    "/team/{team_id}",
    **GET_TEAM_WITH_USERS,
)
async def get_team_with_users(
    crud: TeamServiceDep,
    user: CurrentActiveUser,
    team: Team = Depends(get_team_by_id),
    role_filter: Annotated[UserRole, Query()] = None,
):
    """
    Получить состав команды.

    Args:
        crud: Сервис для работы с командами
        user: Текущий пользователь
        team: ID команды
        role_filter: Фильтрация по роли

    Returns:
        list[TeamSchema]: Список с одной командой и её пользователями
    """
    validate_team_access(user, team)

    return await crud.get_team_with_users(
        team=team,
        role_filter=role_filter,
    )


@router.get(
    "/{team_id}",
    **GET_TEAM,
)
async def get_team(
    team: Team = Depends(get_team_by_id),
):
    """
    Получить команду по ID.

    Args:
        team:

    Returns:
        TeamSchema: одна команда
    """
    return team


@router.post(
    "",
    **CREATE_TEAM,
)
async def create_team(
    crud: TeamServiceDep,
    user: CurrentActiveUser,
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
    ensure_user_is_admin(user)
    ensure_user_not_in_team(user)
    return await crud.create_team(
        team_in=team_in,
        user=user,
    )


@router.post("/{team_id}/user/{user_id}", **ADD_USER_TO_TEAM)
async def add_user_to_team(
    crud: TeamServiceDep,
    current_user: CurrentActiveUser,
    user_id: UserID,
    team: Team = Depends(get_team_by_id),
):
    """
    Добавить пользователя в команду.

    Args:
        crud: Сервис для работы с командами
        current_user: Текущий администратор
        team: ID команды
        user_id: ID пользователя
    """
    user = await get_user_by_id(user_id, session=crud.session)
    check_team_admin(current_user, team)
    ensure_user_not_in_team(user)

    return await crud.add_user_to_team(
        team=team,
        user=user,
    )


@router.patch(
    "/{team_id}/user/{user_id}/role",
    **UPDATE_ROLE_FROM_USER,
)
async def update_user_team_role(
    crud: TeamServiceDep,
    current_user: CurrentActiveUser,
    role_data: UpdateRoleRequest,
    user_id: UserID,
    team: Team = Depends(get_team_by_id),
):
    """
    Добавить роль пользователю в команде.

    Args:
        crud: Сервис для работы с командами
        current_user: Текущий пользователь
        role_data: Данные для обновления роли
        team: ID команды
        user_id: ID пользователя
    """
    user = await get_user_by_id(user_id, session=crud.session)
    check_team_admin(current_user, team)
    ensure_user_in_team(user, team)
    disallow_admin_assignment(role_data)

    return await crud.update_user_team_role(
        user=user,
        role_data=role_data,
    )


@router.delete(
    "/{team_id}/user/{user_id}",
    **REMOVE_USER_FROM_TEAM,
)
async def remove_user_from_team(
    crud: TeamServiceDep,
    current_user: CurrentActiveUser,
    user_id: UserID,
    team: Team = Depends(get_team_by_id),
):
    """
    Удалить пользователя из команды.

    Args:
        crud: Сервис для работы с командами
        current_user: Текущий администратор
        team: ID команды
        user_id: ID пользователя
    """
    user = await get_user_by_id(user_id, session=crud.session)
    validate_team_access(current_user, team)
    ensure_user_in_team(user, team)
    remove_team_admin(user, team)

    return await crud.remove_user_from_team(
        user=user,
    )
