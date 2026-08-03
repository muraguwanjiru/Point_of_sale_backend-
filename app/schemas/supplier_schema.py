from pydantic import BaseModel, Field

class SupplierBase(BaseModel):
    company_name: str = Field(..., max_length=100)
    contact_name: str | None = Field(None, max_length=100)
    phone: str = Field(..., max_length=20)

class SupplierCreate(SupplierBase):
    pass

class SupplierResponse(SupplierBase):
    supplier_id: int

    class Config:
        from_attributes = True
