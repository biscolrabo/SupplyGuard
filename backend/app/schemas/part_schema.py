from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.schemas.supplier_schema import SupplierRead


class PartCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    supplier_id: int
    reference: str = Field(min_length=1, max_length=50)
    lot: str = Field(min_length=1, max_length=50)
    description: str | None = Field(default=None, max_length=255)


class PartUpdate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    reference: str | None = Field(default=None, min_length=1, max_length=50)
    lot: str | None = Field(default=None, min_length=1, max_length=50)
    description: str | None = Field(default=None, max_length=255)

    # Omitir un campo = no cambiarlo; enviarlo como null solo se permite en description
    @field_validator("reference", "lot")
    @classmethod
    def reject_null(cls, value: str | None) -> str:
        if value is None:
            raise ValueError("cannot be null")
        return value


class PartRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    reference: str
    lot: str
    description: str | None
    supplier: SupplierRead
