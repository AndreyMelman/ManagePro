from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime


class MeetingParticipantBase(BaseModel):
    meeting_id: Annotated[int, Field()]
    user_id: Annotated[int, Field()]


class MeetingParticipantCreate(MeetingParticipantBase):
    pass


class MeetingParticipantRead(MeetingParticipantBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime
