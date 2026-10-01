from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.supplier import Supplier


class Part(Base):
    __tablename__ = "parts"
    __table_args__ = (UniqueConstraint("supplier_id", "reference", "lot"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    supplier_id: Mapped[int] = mapped_column(ForeignKey("suppliers.id"), index=True)
    reference: Mapped[str] = mapped_column(String(50))
    lot: Mapped[str] = mapped_column(String(50))
    description: Mapped[str | None] = mapped_column(String(255))

    supplier: Mapped["Supplier"] = relationship(back_populates="parts")
