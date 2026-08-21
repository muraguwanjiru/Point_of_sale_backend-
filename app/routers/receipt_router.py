from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from dependencies import get_current_user
from services.receipt_service import ReceiptService
from schemas.receipt_schema import ReceiptCreate, ReceiptUpdate, ReceiptResponse

router = APIRouter(
    prefix="/receipts",
    tags=["Receipts"],
    dependencies=[Depends(get_current_user)]
)

receipt_service = ReceiptService()


@router.post("/", response_model=ReceiptResponse, status_code=status.HTTP_201_CREATED)
def create_receipt(payload: ReceiptCreate, db: Session = Depends(get_db)):
    return receipt_service.create_receipt(db=db, payload=payload)


@router.get("/", response_model=List[ReceiptResponse])
def read_all_receipts(db: Session = Depends(get_db)):
    return receipt_service.get_all_receipts(db=db)


@router.get("/{receipt_id}", response_model=ReceiptResponse)
def read_receipt(receipt_id: int, db: Session = Depends(get_db)):
    return receipt_service.get_receipt(db=db, receipt_id=receipt_id)


@router.put("/{receipt_id}", response_model=ReceiptResponse)
def update_receipt(receipt_id: int, payload: ReceiptUpdate, db: Session = Depends(get_db)):
    return receipt_service.update_receipt(db=db, receipt_id=receipt_id, payload=payload)


@router.delete("/{receipt_id}", status_code=status.HTTP_200_OK)
def delete_receipt(receipt_id: int, db: Session = Depends(get_db)):
    return receipt_service.delete_receipt(db=db, receipt_id=receipt_id)
