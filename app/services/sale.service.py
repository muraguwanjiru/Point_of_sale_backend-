from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from decimal import Decimal
from repositories.sale_repository import SalesRepository
from schemas.sale_schema import SaleCreate, SaleUpdate

class SaleService:
    def __init__(self):
        self.repository = SalesRepository()

    def get_sale(self, db: Session, sale_id: float):
        sale = self.repository.get(db, sale_id)
        if not sale:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Sale with ID {sale_id} not found"
            )
        return sale

    def get_all_sales(self, db: Session):
        return self.repository.get_all(db)

    def create_sale(self, db: Session, payload: SaleCreate):
        sale_data = payload.model_dump()
        
        try:
            total = Decimal(sale_data.get("total_amount", "0"))
            if total <= 0:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Sale total amount must be greater than zero"
                )
        except (ValueError, TypeError):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid numerical format for total amount"
            )
            
        return self.repository.create(db, sale_data)

    def update_sale(self, db: Session, sale_id: float, payload: SaleUpdate):
        db_obj = self.get_sale(db, sale_id)
        update_data = payload.model_dump(exclude_unset=True)
        
        if "total_amount" in update_data:
            try:
                total = Decimal(update_data["total_amount"])
                if total <= 0:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Updated total amount must be greater than zero"
                    )
            except (ValueError, TypeError):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid numerical format for updated total amount"
                )
                
        return self.repository.update(db, db_obj, update_data)

    def delete_sale(self, db: Session, sale_id: float):
        db_obj = self.get_sale(db, sale_id)
        self.repository.delete(db, db_obj)
        return {"detail": "Sale successfully deleted"}
