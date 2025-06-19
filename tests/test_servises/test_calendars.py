import pytest
from datetime import datetime, date, timedelta
from core.models import Task, Meeting
from core.schemas.task import TaskStatus
from crud.calendars import CalendarService


@pytest.mark.asyncio
async def test_get_month_view_with_events(session):
    team_id = 1
    task = Task(
        title="Task1",
        description="desc",
        creator_id=1,
        team_id=team_id,
        deadline=datetime(2030, 1, 15, 12, 0),
        status=TaskStatus.OPEN,
    )
    meeting = Meeting(
        title="Meeting1",
        description="desc",
        team_id=team_id,
        organizer_id=1,
        start_datetime=datetime(2030, 1, 15, 10, 0),
        end_datetime=datetime(2030, 1, 15, 11, 0),
        is_cancelled=False,
    )
    session.add_all([task, meeting])
    await session.commit()

    crud = CalendarService(session)
    month_view = await crud.get_month_view(2030, 1, team_id)

    day_15 = next((d for d in month_view.days if d.date == date(2030, 1, 15)), None)
    assert day_15 is not None
    event_titles = [e.title for e in day_15.events]
    assert "Task1" in event_titles
    assert "Meeting1" in event_titles


@pytest.mark.asyncio
async def test_get_day_view_with_events(session):
    team_id = 2

    task = Task(
        title="Task2",
        description="desc2",
        creator_id=1,
        team_id=team_id,
        deadline=datetime(2030, 2, 20, 15, 0),
        status=TaskStatus.OPEN,
    )
    meeting = Meeting(
        title="Meeting2",
        description="desc2",
        team_id=team_id,
        organizer_id=1,
        start_datetime=datetime(2030, 2, 20, 9, 0),
        end_datetime=datetime(2030, 2, 20, 10, 0),
        is_cancelled=False,
    )
    session.add_all([task, meeting])
    await session.commit()

    crud = CalendarService(session)
    day_view = await crud.get_day_view(date(2030, 2, 20), team_id)
    event_titles = [e.title for e in day_view.events]
    assert "Task2" in event_titles
    assert "Meeting2" in event_titles


@pytest.mark.asyncio
async def test_get_month_view_no_events(session):
    team_id = 3
    crud = CalendarService(session)
    month_view = await crud.get_month_view(2030, 3, team_id)

    assert all(len(day.events) == 0 for day in month_view.days)


@pytest.mark.asyncio
async def test_get_day_view_no_events(session):
    team_id = 4
    crud = CalendarService(session)
    day_view = await crud.get_day_view(date(2030, 4, 10), team_id)
    assert len(day_view.events) == 0
