from typing import Annotated
from fastapi import (
    Path,
    HTTPException,
    status,
)
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies.params import (
    TaskServiceDep,
    TeamServiceDep,
    CurrentActiveUser,
    TaskCommentServiceDep,
    MeetingServiceDep,
)
from core.models import (
    Task,
    Team,
    TaskComment,
    Meeting,
    User,
)


async def get_user_by_id(
    user_id: Annotated[int, Path()],
    session: AsyncSession,
) -> User:
    stmt = select(User).where(User.id == user_id)
    result = await session.execute(stmt)
    user = result.scalar_one_or_none()
    if user is not None:
        return user
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail={"message": "Пользователь не найден"},
    )


async def get_task_by_id(
    task_id: Annotated[int, Path()],
    crud: TaskServiceDep,
    user: CurrentActiveUser,
) -> Task:
    task = await crud.get_task(
        user=user,
        task_id=task_id,
    )
    if task is not None:
        return task
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail={"message": "Задача не найдена"},
    )


async def get_team_by_id(
    team_id: Annotated[int, Path()],
    crud: TeamServiceDep,
    user: CurrentActiveUser,
) -> Team:
    team = await crud.get_team(
        user=user,
        team_id=team_id,
    )
    if team is not None:
        return team
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail={"message": "Команда не найдена"},
    )


async def get_task_comment_by_id(
    task_id: Annotated[int, Path()],
    comment_id: Annotated[int, Path()],
    crud: TaskCommentServiceDep,
    user: CurrentActiveUser,
) -> TaskComment:
    comment = await crud.get_task_comment(
        task_id=task_id,
        user=user,
        comment_id=comment_id,
    )
    if comment is not None:
        return comment
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail={"message": "Комментарий не найден"},
    )


async def get_meeting_by_id(
    meeting_id: Annotated[int, Path()],
    crud: MeetingServiceDep,
    user: CurrentActiveUser,
) -> Meeting:
    meeting = await crud.get_meeting(
        meeting_id=meeting_id,
        user=user,
    )
    if meeting is not None:
        return meeting
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Встреча с ID {meeting_id} не найдена",
    )
