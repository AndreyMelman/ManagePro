from fastapi import Depends, HTTPException, status
from fastapi_users import FastAPIUsers

from core.models import User
from core.types.role import UserRole
from core.types.user_id import UserIdType

from api.dependencies.authentication import get_user_manager
from api.dependencies.authentication import authentication_backend

fastapi_users = FastAPIUsers[User, UserIdType](
    get_user_manager,
    [authentication_backend],
)

current_active_user = fastapi_users.current_user(active=True)
current_active_superuser = fastapi_users.current_user(active=True, superuser=True)


async def get_user_with_role(
    role: UserRole, user: User = Depends(current_active_user)
) -> User:
    if user.role != role:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Пользователь должен иметь роль - manager",
        )
    return user


async def get_manager(user: User = Depends(current_active_user)) -> User:
    return await get_user_with_role(UserRole.MANAGER, user)


async def get_admin(user: User = Depends(current_active_user)) -> User:
    return await get_user_with_role(UserRole.ADMIN, user)
