from sqlalchemy.ext.asyncio import AsyncSession

from core.models import User
from core.schemas.user import UpdateRoleRequest

from api.api_v1.validators.user_validators import (
    ensure_user_exists,
    disallow_self_role_change,
)


class UserService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def update_user_role(
        self,
        current_user: User,
        role_data: UpdateRoleRequest,
        user_id: int,
    ) -> None:
        user = await self.session.get(User, user_id)

        ensure_user_exists(user)
        disallow_self_role_change(user, current_user)

        user.role = role_data.role
        await self.session.commit()
