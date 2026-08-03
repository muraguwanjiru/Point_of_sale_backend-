from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from repositories.receipt_repository import ReceiptRepository
from schemas.receipt_schema import ReceiptCreate, ReceiptUpdate

class ReceiptService:
    def __init__(self):
        self.repository = ReceiptRepository()

    def get_receipt(self, db: Session, receipt_id: int):
        receipt = self.repository.get(db, receipt_id)
        if not receipt:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Receipt with ID {receipt_id} not found"
            )
        return receipt

    def get_all_receipts(self, db: Session):
        return self.repository.get_all(db)

    def create_receipt(self, db: Session, payload: ReceiptCreate):
        receipt_data = payload.model_dump()
        
        existing_receipt = db.query(self.repository.model).filter(
            self.repository.model.receipt_number == receipt_data["receipt_number"]
        ).first()
        if existing_receipt:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Receipt number already exists"
            )
            
        existing_sale_receipt = db.query(self.repository.model).filter(
            self.repository.model.sale_id == receipt_data["sale_id"]
        ).first()
        if existing_sale_receipt:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A receipt has already been generated for this sale"
            )
            
        return self.repository.create(db, receipt_data)

    def update_receipt(self, db: Session, receipt_id: int, payload: ReceiptUpdate):
        db_obj = self.get_receipt(db, receipt_id)
        update_data = payload.model_dump(exclude_unset=True)
        
        if "receipt_number" in update_data:
            existing_receipt = db.query(self.repository.model).filter(
                self.repository.model.receipt_number == update_data["receipt_number"],
                self.repository.model.receipt_id != receipt_id
            ).first()
            if existing_receipt:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Receipt number is already taken"
                )
                
        return self.repository.update(db, db_obj, update_data)

    def delete_receipt(self, db: Session, receipt_id: int):
        db_obj = self.get_receipt(db, receipt_id)
        self.repository.delete(db, db_obj)
        return {"detail": "Receipt successfully deleted"}
