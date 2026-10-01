from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class SupplierCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    name: str = Field(min_length=1, max_length=100)
    contact_email: EmailStr | None = None


class SupplierUpdate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    name: str | None = Field(default=None, min_length=1, max_length=100)
    contact_email: EmailStr | None = None
    is_active: bool | None = None

    # Omitir un campo = no cambiarlo; enviarlo como null solo se permite en contact_email
    @field_validator("name", "is_active")
    @classmethod
    def reject_null(cls, value: str | bool | None) -> str | bool:
        if value is None:
            raise ValueError("cannot be null")
        return value


class SupplierRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    contact_email: str | None
    is_active: bool
