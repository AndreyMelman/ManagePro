from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, Field, ConfigDict


class EvaluationBaseSchema(BaseModel):
    score: Annotated[int, Field(ge=1, le=5)]
    comment: Annotated[str | None, Field(max_length=1000)] = None


class EvaluationCreateSchema(EvaluationBaseSchema):
    pass


class EvaluationUpdateSchema(BaseModel):
    score: Annotated[int | None, Field(ge=1, le=5)] = None
    comment: Annotated[str | None, Field(max_length=1000)] = None


class EvaluationSchema(EvaluationBaseSchema):
    model_config = ConfigDict(from_attributes=True)

    id: int
    task_id: int
    evaluator_id: int
    user_id: int
    created_at: datetime
    updated_at: datetime


class AverageScoreSchema(BaseModel):
    average_score: float
