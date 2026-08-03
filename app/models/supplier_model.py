from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base

class Supplier(Base):
    __tablename__ = 'suppliers'

    supplier_id = Column(Integer, primary_key=True, autoincrement=True)
    company_name = Column(String(100), nullable=False)
    contact_name = Column(String(100), nullable=True)
    phone = Column(String(20), nullable=False)

    products = relationship("Product", back_populates="supplier")

    def __repr__(self):
        return f"<Supplier(supplier_id={self.supplier_id}, company_name='{self.company_name}')>"
