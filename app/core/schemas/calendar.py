from datetime import datetime, date
from typing import Annotated, List

from pydantic import BaseModel, Field, ConfigDict


class CalendarEventBaseShema(BaseModel):
    title: Annotated[str, Field(max_length=1000)]
    start_datetime: Annotated[datetime, Field()]
    end_datetime: Annotated[datetime, Field()]
    event_type: Annotated[str, Field(max_length=1000)]


class CalendarEventShema(CalendarEventBaseShema):
    model_config = ConfigDict(from_attributes=True)

    id: int
    description: str | None
    status: str | None
    team_id: int


class CalendarDayView(BaseModel):
    date: Annotated[date, Field()]
    events: list[CalendarEventShema]


class CalendarMonthView(BaseModel):
    month: Annotated[int, Field(ge=1)]
    year: Annotated[int, Field(ge=1)]
    days: list[CalendarDayView]
