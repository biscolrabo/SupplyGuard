from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base
from app.models.enums import IncidentStatus, enum_column_type

if TYPE_CHECKING:
    from app.models.incident import Incident
    from app.models.user import User


class IncidentHistory(Base):
    __tablename__ = "incident_history"

    id: Mapped[int] = mapped_column(primary_key=True)
    incident_id: Mapped[int] = mapped_column(ForeignKey("incidents.id"), index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    action: Mapped[str] = mapped_column(String(100))
    from_status: Mapped[IncidentStatus | None] = mapped_column(
        enum_column_type(IncidentStatus, name="from_status")
    )
    to_status: Mapped[IncidentStatus | None] = mapped_column(
        enum_column_type(IncidentStatus, name="to_status")
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    incident: Mapped["Incident"] = relationship(back_populates="history")
    user: Mapped["User"] = relationship()
