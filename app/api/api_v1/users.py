from fastapi import (
    APIRouter,
    HTTPException,
    status,
)

from api.api_v1.fastapi_users import fastapi_users
from api.dependencies.params import Admin, SessionDep
from core.config import settings
from core.models import User, db_helper
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
    session: SessionDep,
    user_id: UserIdType,
    role_data: UpdateRoleRequest,
    admin: Admin,
) -> None:
    user = await session.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    # Проверяем, что суперпользователь не пытается изменить свою роль
    if user.id == admin.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Superuser cannot change their own role",
        )

    # Обновляем роль
    user.role = role_data.role
    await session.commit()
