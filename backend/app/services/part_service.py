from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.exceptions import BusinessRuleError, ConflictError, NotFoundError
from app.models import Part
from app.schemas.part_schema import PartCreate, PartUpdate
from app.services import supplier_service


def list_parts(
    db: Session, supplier_id: int | None = None, reference: str | None = None
) -> list[Part]:
    query = select(Part).order_by(Part.reference, Part.lot)
    if supplier_id is not None:
        query = query.where(Part.supplier_id == supplier_id)
    if reference is not None:
        query = query.where(Part.reference == reference)
    return list(db.scalars(query))


def get_part(db: Session, part_id: int) -> Part:
    part = db.get(Part, part_id)
    if part is None:
        raise NotFoundError("Part", part_id)
    return part


def create_part(db: Session, data: PartCreate) -> Part:
    supplier = supplier_service.get_supplier(db, data.supplier_id)
    if not supplier.is_active:
        raise BusinessRuleError(f"Supplier {supplier.id} is not active")
    _ensure_part_is_unique(db, data.supplier_id, data.reference, data.lot)
    part = Part(**data.model_dump())
    db.add(part)
    db.commit()
    db.refresh(part)
    return part


def update_part(db: Session, part_id: int, data: PartUpdate) -> Part:
    part = get_part(db, part_id)
    changes = data.model_dump(exclude_unset=True)
    if "reference" in changes or "lot" in changes:
        _ensure_part_is_unique(
            db,
            part.supplier_id,
            changes.get("reference", part.reference),
            changes.get("lot", part.lot),
            exclude_id=part_id,
        )
    for field, value in changes.items():
        setattr(part, field, value)
    db.commit()
    db.refresh(part)
    return part


def _ensure_part_is_unique(
    db: Session, supplier_id: int, reference: str, lot: str, exclude_id: int | None = None
) -> None:
    query = select(Part.id).where(
        Part.supplier_id == supplier_id, Part.reference == reference, Part.lot == lot
    )
    if exclude_id is not None:
        query = query.where(Part.id != exclude_id)
    if db.scalar(query) is not None:
        raise ConflictError(f"Part '{reference}' lot '{lot}' already exists for this supplier")
