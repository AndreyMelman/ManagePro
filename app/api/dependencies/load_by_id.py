from typing import Annotated
from fastapi import Path, HTTPException, status
from api.dependencies.params import (
    TaskServiceDep,
    TeamServiceDep,
    CurrentActiveAdmin,
    CurrentActiveUser,
    TaskCommentServiceDep,
    MeetingServiceDep,
)
from core.models import Task, Team, TaskComment, Meeting


async def get_task_by_id(
    task_id: Annotated[int, Path()],
    crud: TaskServiceDep,
    current_user: CurrentActiveUser,
) -> Task:
    task = await crud.get_task(
        current_user=current_user,
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
    current_user: CurrentActiveAdmin,
) -> Team:
    team = await crud.get_team(
        current_user=current_user,
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
    current_user: CurrentActiveUser,
) -> TaskComment:
    comment = await crud.get_task_comment(
        task_id=task_id,
        current_user=current_user,
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
