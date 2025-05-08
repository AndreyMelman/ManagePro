from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, Field, ConfigDict

constr = Annotated[str, Field(min_length=1, max_length=50)]


class TeamBaseSchema(BaseModel):
    name: constr
    description: Annotated[str | None, Field(max_length=1000)] = None
    code: constr


class TeamCreateSchema(TeamBaseSchema):
    """
    Create
    """


class TeamUpdateSchema(TeamBaseSchema):
    """
    Update
    """

    name: constr | None
    description: Annotated[str | None, Field(max_length=1000)] = None
    code: constr | None


class TeamSchema(TeamBaseSchema):
    model_config = ConfigDict(from_attributes=True)

    admin_id: int
    created_at: datetime
    updated_at: datetime
    id: int
