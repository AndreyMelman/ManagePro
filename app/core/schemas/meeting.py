from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, Field, ConfigDict


class MeetingBaseSchema(BaseModel):
    title: Annotated[str, Field(min_length=1, max_length=250)]
    description: Annotated[str | None, Field(max_length=250)] = None
    start_datetime: Annotated[datetime, Field()]
    end_datetime: Annotated[datetime, Field()]


class MeetingCreateSchema(MeetingBaseSchema):
    participants: Annotated[list[int], Field()]


class MeetingUpdateSchema(MeetingBaseSchema):
    title: Annotated[str | None, Field(min_length=1, max_length=250)] = None
    description: Annotated[str | None, Field(max_length=250)] = None
    start_datetime: Annotated[datetime | None, Field()] = None
    end_datetime: Annotated[datetime | None , Field()] = None
    is_cancelled: Annotated[bool | None, Field()] = None
    participants: Annotated[list[int] | None, Field()] = None


class MeetingSchema(MeetingBaseSchema):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime
    organizer_id: int
    team_id: int
    is_cancelled: bool
    participants: list[int]

