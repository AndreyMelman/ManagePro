from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

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
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        if user.id == current_user.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Superuser cannot change their own role",
            )

        user.role = role_data.role
        await self.session.commit()
