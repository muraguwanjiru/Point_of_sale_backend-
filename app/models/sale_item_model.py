from sqlalchemy import Column, Integer, Numeric, ForeignKey
from database import Base
from sqlalchemy.orm import relationship

class SaleItem(Base):
    __tablename__ = 'sale_items'

    sale_item_id = Column(Integer, primary_key=True, autoincrement=True)
    sale_id = Column(Integer, ForeignKey('sales.sale_id'), nullable=False)
    product_id = Column(Integer, ForeignKey('products.product_id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Numeric(10, 2), nullable=False)

    sale = relationship("Sale", back_populates="items")
    product = relationship("Product", back_populates="sale_items")

    def __repr__(self):
        return f"<SaleItem(sale_item_id={self.sale_item_id}, sale_id={self.sale_id}, product_id={self.product_id})>"
