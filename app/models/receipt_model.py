from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base

class Receipt(Base):
    __tablename__ = "receipts"

    receipt_id = Column(Integer, primary_key=True, index=True)
    sale_id = Column(Integer, ForeignKey("sales.sale_id"), unique=True, nullable=False)
    receipt_number = Column(String(50), unique=True, nullable=False)
    issued_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    
    sale = relationship("Sale", back_populates="receipt")