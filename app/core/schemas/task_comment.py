from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, Field, ConfigDict


class TaskCommentBaseSchema(BaseModel):
    content: Annotated[str, Field(min_length=1, max_length=250)]


class TaskCommentCreateSchema(TaskCommentBaseSchema):
    pass


class TaskCommentUpdateSchema(TaskCommentBaseSchema):
    pass


class TaskCommentSchema(TaskCommentBaseSchema):
    model_config = ConfigDict(from_attributes=True)

    id: int
    task_id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
