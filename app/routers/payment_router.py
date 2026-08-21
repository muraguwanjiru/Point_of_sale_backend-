from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from dependencies import get_current_user
from services.payment_service import PaymentService
from schemas.payment_schema import PaymentCreate, PaymentUpdate, PaymentResponse

router = APIRouter(
    prefix="/payments",
    tags=["Payments"],dependencies=[Depends(get_current_user)]
)

payment_service = PaymentService()


@router.post("/", response_model=PaymentResponse, status_code=status.HTTP_201_CREATED)
def create_payment(payload: PaymentCreate, db: Session = Depends(get_db)):
    return payment_service.create_payment(db=db, payload=payload)


@router.get("/", response_model=List[PaymentResponse])
def read_all_payments(db: Session = Depends(get_db)):
    return payment_service.get_all_payments(db=db)


@router.get("/{payment_id}", response_model=PaymentResponse)
def read_payment(payment_id: int, db: Session = Depends(get_db)):
    return payment_service.get_payment(db=db, payment_id=payment_id)


@router.put("/{payment_id}", response_model=PaymentResponse)
def update_payment(payment_id: int, payload: PaymentUpdate, db: Session = Depends(get_db)):
    return payment_service.update_payment(db=db, payment_id=payment_id, payload=payload)


@router.delete("/{payment_id}", status_code=status.HTTP_200_OK)
def delete_payment(payment_id: int, db: Session = Depends(get_db)):
    return payment_service.delete_payment(db=db, payment_id=payment_id)
