from typing import Annotated

from fastapi import APIRouter, Path

from api.api_v1.fastapi_users import fastapi_users
from api.dependencies.params import UserServiceDep, CurrentActiveSuperUser
from core.config import settings

from core.schemas.user import (
    UserRead,
    UserUpdate,
    UpdateRoleRequest,
)

from core.types.user_id import UserIdType

router = APIRouter(
    prefix=settings.api.v1.users,
    tags=["Users"],
)


# /me
# /{id}
router.include_router(
    router=fastapi_users.get_users_router(
        UserRead,
        UserUpdate,
    ),
)


@router.patch("/{user_id}/role")
async def update_user_role(
    crud: UserServiceDep,
    user_id: Annotated[UserIdType, Path()],
    role_data: UpdateRoleRequest,
    admin: CurrentActiveSuperUser,
):
    """
    Изменение роли пользователя

    Args:
        crud: Сервис для работы с командами
        user_id: Текущий пользователь
        role_data:
        admin: Данные для создания команды

    Returns:
        Новая роль у пользователя
    """
    return await crud.update_user_role(
        user_id=user_id,
        role_data=role_data,
        current_user=admin,
    )
