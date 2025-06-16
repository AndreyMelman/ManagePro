from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
    Query,
)

from api.api_v1.validators.meeting_validators import (
    check_meeting_time,
    validate_meeting_participants,
)
from api.dependencies.load_by_id import get_meeting_by_id
from api.dependencies.params import (
    MeetingServiceDep,
    CurrentActiveUser,
)
from core.models import Meeting
from core.schemas.meeting import (
    MeetingCreateSchema,
    MeetingSchema,
    MeetingUpdateSchema,
)
from core.types.role import UserRole
from crud.validators.role_validators import ensure_user_role
from crud.validators.task_validators import ensure_user_has_team
from exceptions.meeting_exceptions import (
    MeetingParticipantValidationError,
    MeetingNotFoundError,
    MeetingPermissionError,
)

router = APIRouter(tags=["Meetings"])


@router.get("", response_model=list[MeetingSchema])
async def get_user_meetings(
    crud: MeetingServiceDep,
    user: CurrentActiveUser,
    skip: Annotated[int, Query()],
    limit: Annotated[int, Query()],
    include_cancelled: bool = False,
):
    ensure_user_has_team(user)
    ensure_user_role(
        user,
        UserRole.MANAGER,
    )
    return await crud.get_user_meetings(
        user=user,
        skip=skip,
        limit=limit,
        include_cancelled=include_cancelled,
    )


@router.get("/{meeting_id}", response_model=MeetingSchema)
async def get_meeting(
    meeting: Meeting = Depends(get_meeting_by_id),
):
    return meeting


@router.post(
    "/meetings",
    response_model=MeetingSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_meeting(
    crud: MeetingServiceDep,
    meeting_in: MeetingCreateSchema,
    user: CurrentActiveUser,
):
    try:
        ensure_user_has_team(user)
        ensure_user_role(
            user,
            UserRole.MANAGER,
        )
        check_meeting_time(meeting_in)
        await validate_meeting_participants(
            session=crud.session,
            participant_ids=meeting_in.participants,
            team_id=user.team_id,
        )
        return await crud.create_meeting(
            meeting_in=meeting_in,
            user=user,
        )
    except MeetingParticipantValidationError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.patch("/{meeting_id}", response_model=MeetingSchema)
async def update_meeting(
    crud: MeetingServiceDep,
    meeting_update: MeetingUpdateSchema,
    user: CurrentActiveUser,
    meeting: Meeting = Depends(get_meeting_by_id),
):
    ensure_user_has_team(user)
    ensure_user_role(
        user,
        UserRole.MANAGER,
    )
    await validate_meeting_participants(
        session=crud.session,
        participant_ids=meeting_update.participants,
        team_id=user.team_id,
    )
    return await crud.update_meeting(
        meeting=meeting,
        meeting_update=meeting_update,
        user=user,
    )


@router.delete("/{meeting_id}", response_model=MeetingSchema)
async def cancel_meeting(
    crud: MeetingServiceDep,
    user: CurrentActiveUser,
    meeting: Meeting = Depends(get_meeting_by_id),
) -> MeetingSchema:
    ensure_user_has_team(user)
    ensure_user_role(
        user,
        UserRole.MANAGER,
    )
    try:
        return await crud.cancel_meeting(
            meeting=meeting,
        )
    except MeetingNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except MeetingPermissionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
