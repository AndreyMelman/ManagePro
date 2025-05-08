from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, Field
from sqlalchemy import Enum


class TaskStatus(str, Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


#
# class TaskBaseSchema(BaseModel):
#     title: Annotated[str, Field(min_length=1, max_length=250)]
#     description: Annotated[str | None, Field(max_length=250)] = None
#     deadline: Annotated[datetime | None, Field()] = "2025-01-01T00:00:00"
#     status: Annotated[TaskStatus, Field()] = TaskStatus.OPEN
