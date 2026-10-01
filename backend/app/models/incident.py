from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base
from app.models.enums import IncidentStatus, Severity, enum_column_type

if TYPE_CHECKING:
    from app.models.action_plan import ActionPlan
    from app.models.incident_history import IncidentHistory
    from app.models.part import Part
    from app.models.user import User


class Incident(Base):
    __tablename__ = "incidents"

    id: Mapped[int] = mapped_column(primary_key=True)
    part_id: Mapped[int] = mapped_column(ForeignKey("parts.id"), index=True)
    reported_by_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    analyzed_by_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"))
    title: Mapped[str] = mapped_column(String(150))
    description: Mapped[str] = mapped_column(Text)
    severity: Mapped[Severity] = mapped_column(enum_column_type(Severity))
    status: Mapped[IncidentStatus] = mapped_column(
        enum_column_type(IncidentStatus, name="status"),
        default=IncidentStatus.OPEN,
        server_default=IncidentStatus.OPEN.value,
        index=True,
    )
    photo_url: Mapped[str | None] = mapped_column(String(500))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    closed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    part: Mapped["Part"] = relationship(back_populates="incidents")
    # Hay dos claves foráneas a users, así que se indica cuál usa cada relación
    reported_by: Mapped["User"] = relationship(foreign_keys=[reported_by_id])
    analyzed_by: Mapped["User | None"] = relationship(foreign_keys=[analyzed_by_id])
    action_plan: Mapped["ActionPlan | None"] = relationship(back_populates="incident")
    history: Mapped[list["IncidentHistory"]] = relationship(
        back_populates="incident", order_by="IncidentHistory.created_at"
    )
