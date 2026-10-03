from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.schemas.task_schema import TaskCreate, TaskRead
from app.schemas.user_schema import UserSummary


class ActionPlanCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    description: str = Field(min_length=1)
    tasks: list[TaskCreate] = []


class ActionPlanUpdate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    description: str | None = Field(default=None, min_length=1)

    @field_validator("description")
    @classmethod
    def reject_null(cls, value: str | None) -> str:
        if value is None:
            raise ValueError("cannot be null")
        return value


class ActionPlanRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    incident_id: int
    description: str
    created_at: datetime
    created_by: UserSummary
    tasks: list[TaskRead]
