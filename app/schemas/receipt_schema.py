from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime

class ReceiptBase(BaseModel):
    sale_id: int
    receipt_number: str = Field(..., max_length=50)


class ReceiptCreate(ReceiptBase):
    pass


class ReceiptUpdate(BaseModel):
    sale_id: int | None = None
    receipt_number: str | None = Field(default=None, max_length=50)


class ReceiptResponse(ReceiptBase):
    receipt_id: int
    issued_at: datetime
    model_config = ConfigDict(from_attributes=True)
