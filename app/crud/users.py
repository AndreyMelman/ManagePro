from sqlalchemy.ext.asyncio import AsyncSession

from core.models import User
from core.schemas.user import UpdateRoleRequest


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
