from sqlalchemy import Column, Integer, String
from database import Base
from sqlalchemy.orm import relationship

class Category(Base):
    __tablename__ = "categories"

    category_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
    description = Column(String(100), nullable=True)
    

    products = relationship("Product", back_populates="category")
