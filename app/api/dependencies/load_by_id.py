from typing import Annotated
from fastapi import Path
from api.dependencies.params import (
    TaskServiceDep,
    TeamServiceDep,
    CurrentActiveAdmin,
    CurrentActiveUser,
)
from core.models import Task, Team
from exceptions.task_exceptions import TaskNotFoundError
from exceptions.team_exceptions import TeamNotFoundError


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
    raise TaskNotFoundError()


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
    raise TeamNotFoundError()
