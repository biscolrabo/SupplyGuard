from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.models.enums import IncidentStatus, Severity
from app.schemas.action_plan_schema import ActionPlanRead
from app.schemas.incident_history_schema import IncidentHistoryRead
from app.schemas.part_schema import PartRead
from app.schemas.user_schema import UserSummary


class IncidentCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    part_id: int
    title: str = Field(min_length=1, max_length=150)
    description: str = Field(min_length=1)
    severity: Severity
    photo_url: str | None = Field(default=None, max_length=500)


class IncidentUpdate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    title: str | None = Field(default=None, min_length=1, max_length=150)
    description: str | None = Field(default=None, min_length=1)
    severity: Severity | None = None
    photo_url: str | None = Field(default=None, max_length=500)

    # Omitir un campo = no cambiarlo; enviarlo como null solo se permite en photo_url
    @field_validator("title", "description", "severity")
    @classmethod
    def reject_null(cls, value: str | Severity | None) -> str | Severity:
        if value is None:
            raise ValueError("cannot be null")
        return value


class IncidentStatusChange(BaseModel):
    status: IncidentStatus


class IncidentRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str
    severity: Severity
    status: IncidentStatus
    photo_url: str | None
    created_at: datetime
    closed_at: datetime | None
    part: PartRead
    reported_by: UserSummary
    analyzed_by: UserSummary | None


class IncidentDetail(IncidentRead):
    action_plan: ActionPlanRead | None
    history: list[IncidentHistoryRead]
