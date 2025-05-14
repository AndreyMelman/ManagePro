from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, Field, ConfigDict
from enum import Enum


class TaskStatus(str, Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class TaskBaseSchema(BaseModel):
    title: Annotated[str, Field(min_length=1, max_length=250)]
    description: Annotated[str | None, Field(max_length=250)] = None
    deadline: Annotated[datetime | None, Field()] = "2025-01-01T00:00:00"
    status: Annotated[TaskStatus, Field()] = TaskStatus.OPEN
    creator_id: Annotated[int, Field()]
    assignee_id: Annotated[int | None, Field()] = None
    team_id: Annotated[int, Field()]


class TaskCreateShema(BaseModel):
    title: Annotated[str, Field(min_length=1, max_length=250)]
    description: Annotated[str | None, Field(max_length=250)] = None
    deadline: Annotated[datetime | None, Field()] = "2025-01-01T00:00:00"
    status: Annotated[TaskStatus, Field()] = TaskStatus.OPEN
    assignee_id: Annotated[int | None, Field()] = None


class TaskUpdateShema(BaseModel):
    title: Annotated[str | None, Field(min_length=1, max_length=250)] = None
    description: Annotated[str | None, Field(max_length=250)] = None
    deadline: Annotated[datetime | None, Field()] = "2025-01-01T00:00:00"
    status: Annotated[TaskStatus | None, Field()] = TaskStatus.OPEN


class TaskSchema(TaskBaseSchema):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime
