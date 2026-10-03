from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.supplier_schema import SupplierCreate, SupplierRead, SupplierUpdate
from app.services import supplier_service

router = APIRouter(prefix="/suppliers", tags=["suppliers"])

DbSession = Annotated[Session, Depends(get_db)]


@router.get("", response_model=list[SupplierRead])
def list_suppliers(db: DbSession, active: bool | None = None):
    return supplier_service.list_suppliers(db, active)


@router.get("/{supplier_id}", response_model=SupplierRead)
def get_supplier(supplier_id: int, db: DbSession):
    return supplier_service.get_supplier(db, supplier_id)


@router.post("", response_model=SupplierRead, status_code=status.HTTP_201_CREATED)
def create_supplier(data: SupplierCreate, db: DbSession):
    return supplier_service.create_supplier(db, data)


@router.patch("/{supplier_id}", response_model=SupplierRead)
def update_supplier(supplier_id: int, data: SupplierUpdate, db: DbSession):
    return supplier_service.update_supplier(db, supplier_id, data)
