from pydantic import BaseModel, Field, ConfigDict
from decimal import Decimal

class ProductBase(BaseModel):
    barcode: str = Field(..., max_length=50)
    name: str = Field(..., max_length=100)
    price: Decimal = Field(..., gt=0, max_digits=10, decimal_places=2)
    stock_quantity: int = Field(default=0, ge=0)
    category_id: int = Field(...)
    supplier_id: int = Field(...)


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    barcode: str | None = Field(default=None, max_length=50)
    name: str | None = Field(default=None, max_length=100)
    price: Decimal | None = Field(default=None, gt=0, max_digits=10, decimal_places=2)
    stock_quantity: int | None = Field(default=None, ge=0)
    category_id: int | None = None
    supplier_id: int | None = None


class ProductResponse(ProductBase):
    product_id: int
    model_config = ConfigDict(from_attributes=True)
