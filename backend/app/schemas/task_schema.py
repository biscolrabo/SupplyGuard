from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.schemas.user_schema import UserSummary


class TaskCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    title: str = Field(min_length=1, max_length=150)
    assigned_to_id: int
    due_date: date


class TaskUpdate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    title: str | None = Field(default=None, min_length=1, max_length=150)
    assigned_to_id: int | None = None
    due_date: date | None = None
    completed: bool | None = None

    @field_validator("title", "assigned_to_id", "due_date", "completed")
    @classmethod
    def reject_null(cls, value: str | int | date | bool | None) -> str | int | date | bool:
        if value is None:
            raise ValueError("cannot be null")
        return value


class TaskRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    action_plan_id: int
    title: str
    due_date: date
    completed_at: datetime | None
    assigned_to: UserSummary
