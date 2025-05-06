from typing import Annotated

from fastapi import Depends
from fastapi_users import schemas
from pydantic import BaseModel

from core.types.role import UserRole
from core.types.user_id import UserIdType


class UserRead(schemas.BaseUser[UserIdType]):
    role: Annotated[UserRole, Depends()]


class UserCreate(schemas.BaseUserCreate):
    pass


class UserUpdate(schemas.BaseUserUpdate):
    pass


class UpdateRoleRequest(BaseModel):
    role: Annotated[UserRole, Depends()]


class SuperUserCreate(UserCreate):
    role: Annotated[UserRole, Depends()]
