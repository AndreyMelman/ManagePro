from sqlalchemy.ext.asyncio import AsyncSession

from core.models import User
from core.schemas.user import UpdateRoleRequest

from .validators.permissions import (
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
        """
        Обновить роль пользователя.

        Args:
            current_user: Текущий администратор команды
            role_data: Команда где нужно обновить роль пользователя
            user_id: ID пользователя

        Raises:
            ensure_user_exists: Если пользователь не состоит в команде
            disallow_self_role_change: Если пользователь - это администратор
        """
        user = await self.session.get(User, user_id)

        await ensure_user_exists(user)
        await disallow_self_role_change(user, current_user)

        user.role = role_data.role
        await self.session.commit()
