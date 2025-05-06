from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.fastapi_users import (
    current_active_user,
    get_manager,
    current_active_superuser,
)
from core.models import (
    User,
    db_helper,
)

SessionDep = Annotated[AsyncSession, Depends(db_helper.session_getter)]
CurrentActiveUser = Annotated[User, Depends(current_active_user)]
Manager = Annotated[User, Depends(get_manager)]
Admin = Annotated[User, Depends(current_active_superuser)]
