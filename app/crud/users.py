from sqlalchemy.ext.asyncio import AsyncSession

from exceptions.user_exceptions import (
    UserNotFoundError,
    UserCannotChangeRole,
)
from core.models import User
from core.schemas.user import UpdateRoleRequest


class UserService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def update_user_role(
        self,
        user_id: int,
        current_user: User,
        role_data: UpdateRoleRequest,
    ) -> None:
        user = await self.session.get(User, user_id)

        if not user:
            raise UserNotFoundError()

        if user.id == current_user.id:
            raise UserCannotChangeRole()

        user.role = role_data.role
        await self.session.commit()
