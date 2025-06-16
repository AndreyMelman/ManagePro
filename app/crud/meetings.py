from datetime import datetime

from sqlalchemy import (
    select,
    delete,
    or_,
    and_,
)
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import (
    Meeting,
    User,
    MeetingParticipant,
)
from core.schemas.meeting import (
    MeetingCreateSchema,
    MeetingUpdateSchema,
)
from exceptions.meeting_exceptions import MeetingTimeConflictError


class MeetingService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_meeting(
        self,
        meeting_in: MeetingCreateSchema,
        user: User,
    ) -> Meeting:
        # Проверяем наложение времени для всех участников
        for participant_id in meeting_in.participants:
            await self._check_time_conflicts(
                user=await self.session.get(User, participant_id),
                start_datetime=meeting_in.start_datetime,
                end_datetime=meeting_in.end_datetime,
            )

        # Создаем встречу
        meeting = Meeting(
            title=meeting_in.title,
            description=meeting_in.description,
            start_datetime=meeting_in.start_datetime,
            end_datetime=meeting_in.end_datetime,
            team_id=user.team_id,
            organizer_id=user.id,
        )
        self.session.add(meeting)
        await self.session.flush()

        # Добавляем участников
        for user_id in meeting_in.participants:
            participant = MeetingParticipant(meeting_id=meeting.id, user_id=user_id)
            self.session.add(participant)

        await self.session.commit()

        return meeting

    async def get_meeting(
        self,
        meeting_id: int,
        user: User,
    ) -> Meeting:
        stmt = select(Meeting).where(
            Meeting.id == meeting_id,
            Meeting.organizer_id == user.id,
        )
        result = await self.session.execute(stmt)
        meeting = result.scalars().first()

        return meeting

    async def get_user_meetings(
        self,
        user: User,
        skip: int = 0,
        limit: int = 100,
        include_cancelled: bool = False,
    ) -> list[Meeting]:
        stmt = (
            select(Meeting)
            .join(MeetingParticipant)
            .where(MeetingParticipant.user_id == user.id)
        )

        if not include_cancelled:
            stmt = stmt.where(Meeting.is_cancelled == False)

        stmt = stmt.offset(skip).limit(limit)
        result = await self.session.execute(stmt)
        meeting = result.scalars().all()
        return list(meeting)

    async def update_meeting(
        self,
        meeting: Meeting,
        meeting_update: MeetingUpdateSchema,
        user: User,
    ) -> Meeting:
        if meeting_update.start_datetime or meeting_update.end_datetime:
            await self._check_time_conflicts(
                user,
                meeting_update.start_datetime or meeting.start_datetime,
                meeting_update.end_datetime or meeting.end_datetime,
                exclude_meeting_id=meeting.id,
            )

        for field, value in meeting_update.model_dump(exclude_unset=True).items():
            if field != "participants":
                setattr(meeting, field, value)

        if meeting_update.participants is not None:
            await self.session.execute(
                delete(MeetingParticipant).where(
                    MeetingParticipant.meeting_id == meeting.id
                )
            )
            for user_id in meeting_update.participants:
                participant = MeetingParticipant(meeting_id=meeting.id, user_id=user_id)
                self.session.add(participant)

        await self.session.commit()
        return meeting

    async def cancel_meeting(
        self,
        meeting: Meeting,
    ) -> Meeting:
        meeting.is_cancelled = True
        await self.session.commit()
        return meeting

    async def _check_time_conflicts(
        self,
        user: User,
        start_datetime: datetime,
        end_datetime: datetime,
        exclude_meeting_id: int | None = None,
    ) -> None:
        """Проверка наложения времени встреч"""
        query = (
            select(Meeting)
            .join(MeetingParticipant)
            .where(
                MeetingParticipant.user_id == user.id,
                Meeting.is_cancelled == False,
                or_(
                    and_(
                        Meeting.start_datetime <= start_datetime,
                        Meeting.end_datetime > start_datetime,
                    ),
                    and_(
                        Meeting.start_datetime < end_datetime,
                        Meeting.end_datetime >= end_datetime,
                    ),
                    and_(
                        Meeting.start_datetime >= start_datetime,
                        Meeting.end_datetime <= end_datetime,
                    ),
                ),
            )
        )

        if exclude_meeting_id:
            query = query.where(Meeting.id != exclude_meeting_id)

        result = await self.session.execute(query)
        conflicting_meetings = result.scalars().all()

        if conflicting_meetings:
            raise MeetingTimeConflictError(
                "У вас уже есть встречи, которые накладываются по времени"
            )
