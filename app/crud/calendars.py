from datetime import datetime, date
from calendar import monthcalendar

from sqlalchemy import select, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Task, Meeting
from core.schemas.calendar import (
    CalendarEventShema,
    CalendarDayView,
    CalendarMonthView,
)


class CalendarService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_month_view(
        self,
        year: int,
        month: int,
        team_id: int,
    ) -> CalendarMonthView:
        cal = monthcalendar(year, month)

        days = []
        for week in cal:
            for day in week:
                if day != 0:
                    current_date = date(year, month, day)
                    events = await self._get_events_for_date(current_date, team_id)
                    days.append(CalendarDayView(date=current_date, events=events))

        return CalendarMonthView(
            month=month,
            year=year,
            days=days,
        )

    async def get_day_view(
        self,
        day_date: date,
        team_id: int,
    ) -> CalendarDayView:
        events = await self._get_events_for_date(day_date, team_id)
        return CalendarDayView(date=day_date, events=events)

    async def _get_events_for_date(
        self,
        day_date: date,
        team_id: int,
    ) -> list[CalendarEventShema]:
        start_datetime = datetime.combine(day_date, datetime.min.time())
        end_datetime = datetime.combine(day_date, datetime.max.time())

        tasks_query = select(Task).where(
            and_(
                Task.team_id == team_id,
                Task.deadline >= start_datetime,
                Task.deadline <= end_datetime,
            )
        )
        tasks = (await self.session.execute(tasks_query)).scalars().all()

        meetings_query = select(Meeting).where(
            and_(
                Meeting.team_id == team_id,
                Meeting.is_cancelled == False,
                or_(
                    and_(
                        Meeting.start_datetime >= start_datetime,
                        Meeting.start_datetime <= end_datetime,
                    ),
                    and_(
                        Meeting.end_datetime >= start_datetime,
                        Meeting.end_datetime <= end_datetime,
                    ),
                ),
            )
        )
        meetings = (await self.session.execute(meetings_query)).scalars().all()

        events = []

        for task in tasks:
            events.append(
                CalendarEventShema(
                    id=task.id,
                    title=task.title,
                    description=task.description,
                    start_datetime=task.deadline,
                    end_datetime=task.deadline,
                    event_type="task",
                    status=task.status,
                    team_id=task.team_id,
                )
            )

        for meeting in meetings:
            events.append(
                CalendarEventShema(
                    id=meeting.id,
                    title=meeting.title,
                    description=meeting.description,
                    start_datetime=meeting.start_datetime,
                    end_datetime=meeting.end_datetime,
                    event_type="meeting",
                    status=None,
                    team_id=meeting.team_id,
                )
            )

        return sorted(events, key=lambda x: x.start_datetime)
