from core.models import db_helper
from typing import TypeVar, Callable, Annotated, Type
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

T = TypeVar("T")


def make_crud_dependency(crud_class: Type[T]) -> Callable[[AsyncSession], T]:
    def _get_crud(
        session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    ) -> T:
        return crud_class(session)

    return _get_crud
