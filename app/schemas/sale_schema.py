from pydantic import BaseModel, Field, ConfigDict
from decimal import Decimal

class SaleBase(BaseModel):
    sale_id: Decimal = Field(..., max_digits=10, decimal_places=2)
    total_amount: str = Field(..., max_length=100)
    customer_id: int | None = None
    user_id: int


class SaleCreate(SaleBase):
    pass


class SaleUpdate(BaseModel):
    sale_id: Decimal | None = Field(default=None, max_digits=10, decimal_places=2)
    total_amount: str | None = Field(default=None, max_length=100)
    customer_id: int | None = None
    user_id: int | None = None


class SaleResponse(SaleBase):
    model_config = ConfigDict(from_attributes=True)
