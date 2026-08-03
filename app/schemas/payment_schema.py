from pydantic import BaseModel, Field, ConfigDict
from decimal import Decimal
from datetime import datetime

class PaymentBase(BaseModel):
    sale_id: int
    payment_method: str = Field(..., max_length=30)
    amount_paid: Decimal = Field(..., gt=0, max_digits=10, decimal_places=2)


class PaymentCreate(PaymentBase):
    pass


class PaymentUpdate(BaseModel):
    sale_id: int | None = None
    payment_method: str | None = Field(default=None, max_length=30)
    amount_paid: Decimal | None = Field(default=None, gt=0, max_digits=10, decimal_places=2)


class PaymentResponse(PaymentBase):
    payment_id: int
    payment_date: datetime

    model_config = ConfigDict(from_attributes=True)
