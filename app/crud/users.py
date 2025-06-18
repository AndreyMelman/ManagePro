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
        user: User,
        role_data: UpdateRoleRequest,
    ) -> None:
        user.role = role_data.role
        await self.session.commit()
