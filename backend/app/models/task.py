from datetime import date, datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.action_plan import ActionPlan
    from app.models.user import User


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    action_plan_id: Mapped[int] = mapped_column(ForeignKey("action_plans.id"), index=True)
    assigned_to_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    title: Mapped[str] = mapped_column(String(150))
    due_date: Mapped[date]
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    action_plan: Mapped["ActionPlan"] = relationship(back_populates="tasks")
    assigned_to: Mapped["User"] = relationship()
