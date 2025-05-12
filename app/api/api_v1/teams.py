from fastapi import APIRouter, status

from api.dependencies.params import (
    TeamServiceDep,
    CurrentActiveAdmin,
    CurrentActiveUser,
)
from core.schemas.team import TeamCreateSchema, TeamSchema
from core.schemas.user import UserCreate, UserRead
from crud import teams

router = APIRouter(tags=["Teams"])


@router.get(
    "/",
)
async def get_team_with_users(
    crud: TeamServiceDep,
    user: CurrentActiveAdmin,
    team_id: int,
):
    return await crud.get_team_with_users(
        team_id=team_id,
        current_user=user,
    )


@router.post(
    "",
    response_model=TeamSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_team(
    crud: TeamServiceDep,
    user: CurrentActiveAdmin,
    team_in: TeamCreateSchema,
):
    return await crud.create_team(
        user=user,
        team_in=team_in,
    )


@router.post(
    "/{team_id}/user/{user_id}",
    status_code=status.HTTP_201_CREATED,
)
async def add_user_to_team(
    crud: TeamServiceDep,
    user: CurrentActiveAdmin,
    team_id: int,
    user_id: int,
):
    return await crud.add_user_to_team(
        current_user=user,
        team_id=team_id,
        user_id=user_id,
    )


@router.delete(
    "/{team_id}/user/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def remove_user_from_team(
    crud: TeamServiceDep,
    user: CurrentActiveAdmin,
    team_id: int,
    user_id: int,
):
    return await crud.remove_user_from_team(
        current_user=user,
        team_id=team_id,
        user_id=user_id,
    )
