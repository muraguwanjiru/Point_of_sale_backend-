from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from repositories.payment_repository import PaymentRepository
from schemas.payment_schema import PaymentCreate, PaymentUpdate

class PaymentService:
    def __init__(self):
        self.repository = PaymentRepository()

    def get_payment(self, db: Session, payment_id: int):
        payment = self.repository.get(db, payment_id)
        if not payment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Payment record with ID {payment_id} not found"
            )
        return payment

    def get_all_payments(self, db: Session):
        return self.repository.get_all(db)

    def create_payment(self, db: Session, payload: PaymentCreate):
        payment_data = payload.model_dump()
        return self.repository.create(db, payment_data)

    def update_payment(self, db: Session, payment_id: int, payload: PaymentUpdate):
        db_obj = self.get_payment(db, payment_id)
        update_data = payload.model_dump(exclude_unset=True)
        return self.repository.update(db, db_obj, update_data)

    def delete_payment(self, db: Session, payment_id: int):
        db_obj = self.get_payment(db, payment_id)
        self.repository.delete(db, db_obj)
        return {"detail": "Payment record successfully deleted"}
