from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

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

    async def get_user_by_email(self, email: str) -> User | None:
        stmt = select(User).where(User.email == email)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_user_by_id(self, user_id: int) -> User | None:
        stmt = select(User).where(User.id == user_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
