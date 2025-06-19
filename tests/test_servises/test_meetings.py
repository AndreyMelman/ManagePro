import pytest
from datetime import datetime, timedelta
from core.models import User
from core.types.role import UserRole
from core.schemas.meeting import MeetingCreateSchema, MeetingUpdateSchema
from crud.meetings import MeetingService
from exceptions.meeting_exceptions import MeetingTimeConflictError


@pytest.mark.asyncio
async def test_create_meeting(session):
    user = User(email="manager@ex.com", role=UserRole.MANAGER, team_id=1)
    participant = User(email="user@ex.com", role=UserRole.USER, team_id=1)
    session.add_all([user, participant])
    await session.commit()
    await session.refresh(user)
    await session.refresh(participant)

    crud = MeetingService(session)
    start = datetime(2030, 1, 1, 10, 0)
    end = datetime(2030, 1, 1, 11, 0)
    meeting_in = MeetingCreateSchema(
        title="Встреча",
        description="Описание",
        start_datetime=start,
        end_datetime=end,
        participants=[participant.id],
    )
    meeting = await crud.create_meeting(meeting_in, user)
    assert meeting.title == "Встреча"
    assert meeting.team_id == user.team_id
    assert meeting.organizer_id == user.id


@pytest.mark.asyncio
async def test_create_meeting_time_conflict(session):
    user = User(email="manager2@ex.com", role=UserRole.MANAGER, team_id=2)
    session.add(user)
    await session.commit()
    await session.refresh(user)

    crud = MeetingService(session)
    start = datetime(2030, 1, 1, 10, 0)
    end = datetime(2030, 1, 1, 11, 0)

    meeting_in1 = MeetingCreateSchema(
        title="Встреча1",
        description="",
        start_datetime=start,
        end_datetime=end,
        participants=[user.id],
    )
    await crud.create_meeting(meeting_in1, user)

    meeting_in2 = MeetingCreateSchema(
        title="Встреча2",
        description="",
        start_datetime=start + timedelta(minutes=30),
        end_datetime=end + timedelta(minutes=30),
        participants=[user.id],
    )
    with pytest.raises(MeetingTimeConflictError):
        await crud.create_meeting(meeting_in2, user)


@pytest.mark.asyncio
async def test_get_meeting(session):
    user = User(email="manager3@ex.com", role=UserRole.MANAGER, team_id=3)
    session.add(user)
    await session.commit()
    await session.refresh(user)

    crud = MeetingService(session)
    start = datetime(2030, 1, 2, 10, 0)
    end = datetime(2030, 1, 2, 11, 0)
    meeting_in = MeetingCreateSchema(
        title="Встреча3",
        description="",
        start_datetime=start,
        end_datetime=end,
        participants=[user.id],
    )
    meeting = await crud.create_meeting(meeting_in, user)
    found = await crud.get_meeting(meeting.id, user)
    assert found.id == meeting.id
    assert found.title == "Встреча3"


@pytest.mark.asyncio
async def test_get_user_meetings(session):
    user = User(email="manager4@ex.com", role=UserRole.MANAGER, team_id=4)
    session.add(user)
    await session.commit()
    await session.refresh(user)

    crud = MeetingService(session)
    start = datetime(2030, 1, 3, 10, 0)
    end = datetime(2030, 1, 3, 11, 0)
    meeting_in = MeetingCreateSchema(
        title="Встреча4",
        description="",
        start_datetime=start,
        end_datetime=end,
        participants=[user.id],
    )
    await crud.create_meeting(meeting_in, user)
    meetings = await crud.get_user_meetings(user)
    assert len(meetings) >= 1
    assert any(m.title == "Встреча4" for m in meetings)


@pytest.mark.asyncio
async def test_update_meeting(session):
    user = User(email="manager5@ex.com", role=UserRole.MANAGER, team_id=5)
    session.add(user)
    await session.commit()
    await session.refresh(user)

    crud = MeetingService(session)
    start = datetime(2030, 1, 4, 10, 0)
    end = datetime(2030, 1, 4, 11, 0)
    meeting_in = MeetingCreateSchema(
        title="Встреча5",
        description="",
        start_datetime=start,
        end_datetime=end,
        participants=[user.id],
    )
    meeting = await crud.create_meeting(meeting_in, user)
    update_in = MeetingUpdateSchema(title="Обновлено")
    updated = await crud.update_meeting(meeting, update_in, user)
    assert updated.title == "Обновлено"


@pytest.mark.asyncio
async def test_cancel_meeting(session):
    user = User(email="manager6@ex.com", role=UserRole.MANAGER, team_id=6)
    session.add(user)
    await session.commit()
    await session.refresh(user)

    crud = MeetingService(session)
    start = datetime(2030, 1, 5, 10, 0)
    end = datetime(2030, 1, 5, 11, 0)
    meeting_in = MeetingCreateSchema(
        title="Встреча6",
        description="",
        start_datetime=start,
        end_datetime=end,
        participants=[user.id],
    )
    meeting = await crud.create_meeting(meeting_in, user)
    cancelled = await crud.cancel_meeting(meeting)
    assert cancelled.is_cancelled is True
