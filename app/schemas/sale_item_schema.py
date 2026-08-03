from pydantic import BaseModel, Field
from decimal import Decimal

class SaleItemBase(BaseModel):
    sale_id: int
    product_id: int
    quantity: int = Field(..., gt=0)
    unit_price: Decimal = Field(..., max_digits=10, decimal_places=2, ge=0)

class SaleItemCreate(SaleItemBase):
    pass

class SaleItemResponse(SaleItemBase):
    sale_item_id: int

    class Config:
        from_attributes = True
