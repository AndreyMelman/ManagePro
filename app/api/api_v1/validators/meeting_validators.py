from fastapi import HTTPException, status
from sqlalchemy import select, or_, and_
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import User, Meeting, MeetingParticipant
from core.schemas.meeting import MeetingCreateSchema
from exceptions.meeting_exceptions import MeetingParticipantValidationError


def check_meeting_time(
    meeting_in: MeetingCreateSchema,
) -> None:
    if meeting_in.end_datetime <= meeting_in.start_datetime:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Время окончания встречи должно быть позже времени начала",
        )


async def validate_meeting_participants(
    session: AsyncSession, participant_ids: list[int], team_id: int
) -> None:
    participants_query = select(User).where(
        User.id.in_(participant_ids), User.team_id == team_id
    )
    result = await session.execute(participants_query)
    found_participants = result.scalars().all()

    if len(found_participants) != len(participant_ids):
        raise MeetingParticipantValidationError(
            "Некоторые участники не найдены или не состоят в вашей команде"
        )
