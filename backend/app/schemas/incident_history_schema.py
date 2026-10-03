from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.models.enums import IncidentStatus
from app.schemas.user_schema import UserSummary


class IncidentHistoryRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    action: str
    from_status: IncidentStatus | None
    to_status: IncidentStatus | None
    created_at: datetime
    user: UserSummary
