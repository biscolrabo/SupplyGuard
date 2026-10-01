from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.exceptions import ConflictError, NotFoundError
from app.models import Supplier
from app.schemas.supplier import SupplierCreate, SupplierUpdate


def list_suppliers(db: Session, active: bool | None = None) -> list[Supplier]:
    query = select(Supplier).order_by(Supplier.name)
    if active is not None:
        query = query.where(Supplier.is_active == active)
    return list(db.scalars(query))


def get_supplier(db: Session, supplier_id: int) -> Supplier:
    supplier = db.get(Supplier, supplier_id)
    if supplier is None:
        raise NotFoundError("Supplier", supplier_id)
    return supplier


def create_supplier(db: Session, data: SupplierCreate) -> Supplier:
    _ensure_name_is_free(db, data.name)
    supplier = Supplier(**data.model_dump())
    db.add(supplier)
    db.commit()
    db.refresh(supplier)
    return supplier


def update_supplier(db: Session, supplier_id: int, data: SupplierUpdate) -> Supplier:
    supplier = get_supplier(db, supplier_id)
    changes = data.model_dump(exclude_unset=True)
    if "name" in changes:
        _ensure_name_is_free(db, changes["name"], exclude_id=supplier_id)
    for field, value in changes.items():
        setattr(supplier, field, value)
    db.commit()
    db.refresh(supplier)
    return supplier


def _ensure_name_is_free(db: Session, name: str, exclude_id: int | None = None) -> None:
    # Sin distinguir mayúsculas: "Metalex" y "METALEX" son el mismo proveedor
    query = select(Supplier.id).where(func.lower(Supplier.name) == name.lower())
    if exclude_id is not None:
        query = query.where(Supplier.id != exclude_id)
    if db.scalar(query) is not None:
        raise ConflictError(f"Supplier '{name}' already exists")
