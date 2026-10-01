from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.incident import Incident
    from app.models.task import Task
    from app.models.user import User


class ActionPlan(Base):
    __tablename__ = "action_plans"

    id: Mapped[int] = mapped_column(primary_key=True)
    incident_id: Mapped[int] = mapped_column(ForeignKey("incidents.id"), unique=True)
    created_by_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    description: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    incident: Mapped["Incident"] = relationship(back_populates="action_plan")
    created_by: Mapped["User"] = relationship()
    # Las tareas pertenecen al plan: si se quitan de la lista, se borran
    tasks: Mapped[list["Task"]] = relationship(
        back_populates="action_plan", cascade="all, delete-orphan", order_by="Task.due_date"
    )
