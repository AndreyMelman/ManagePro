import pytest
from core.models import User
from core.types.role import UserRole
from core.schemas.user import UpdateRoleRequest
from crud.users import UserService


@pytest.mark.asyncio
async def test_update_user_role(session):
    user = User(email="user@ex.com", role=UserRole.USER)
    session.add(user)
    await session.commit()
    await session.refresh(user)

    crud = UserService(session)
    role_data = UpdateRoleRequest(role=UserRole.MANAGER)
    await crud.update_user_role(user, role_data)
    await session.refresh(user)
    assert user.role == UserRole.MANAGER
