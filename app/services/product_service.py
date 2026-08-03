from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from repositories.product_repository import ProductRepository
from schemas.product_schema import ProductCreate, ProductUpdate

class ProductService:
    def __init__(self):
        self.repository = ProductRepository()

    def get_product(self, db: Session, product_id: int):
        product = self.repository.get(db, product_id)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product with ID {product_id} not found"
            )
        return product

    def get_all_products(self, db: Session):
        return self.repository.get_all(db)

    def create_product(self, db: Session, payload: ProductCreate):
        product_data = payload.model_dump()
        
        if product_data.get("price") is not None and product_data["price"] <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Product price must be greater than zero"
            )
            
        if product_data.get("stock_quantity") is not None and product_data["stock_quantity"] < 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Stock quantity cannot be negative"
            )
            
        return self.repository.create(db, product_data)

    def update_product(self, db: Session, product_id: int, payload: ProductUpdate):
        db_obj = self.get_product(db, product_id)
        update_data = payload.model_dump(exclude_unset=True)
        
        if "price" in update_data and update_data["price"] <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Updated product price must be greater than zero"
            )
            
        if "stock_quantity" in update_data and update_data["stock_quantity"] < 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Updated stock quantity cannot be negative"
            )
            
        return self.repository.update(db, db_obj, update_data)

    def delete_product(self, db: Session, product_id: int):
        db_obj = self.get_product(db, product_id)
        
        if getattr(db_obj, "stock_quantity", 0) > 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot delete a product that still has stock remaining"
            )
            
        self.repository.delete(db, db_obj)
        return {"detail": "Product successfully deleted"}
