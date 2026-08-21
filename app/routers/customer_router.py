from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from dependencies import get_current_user
from services.customer_service import CustomerService
from schemas.customer_schema import CustomerCreate, CustomerUpdate, CustomerResponse

router = APIRouter(
    prefix="/customers",
    tags=["Customers"],dependencies=[Depends(get_current_user)]
)

customer_service = CustomerService()


@router.post("/", response_model=CustomerResponse, status_code=status.HTTP_201_CREATED)
def create_customer(payload: CustomerCreate, db: Session = Depends(get_db)):
    return customer_service.create_customer(db=db, payload=payload)


@router.get("/", response_model=List[CustomerResponse])
def read_all_customers(db: Session = Depends(get_db)):
    return customer_service.get_all_customers(db=db)


@router.get("/{customer_id}", response_model=CustomerResponse)
def read_customer(customer_id: int, db: Session = Depends(get_db)):
    return customer_service.get_customer(db=db, customer_id=customer_id)


@router.put("/{customer_id}", response_model=CustomerResponse)
def update_customer(customer_id: int, payload: CustomerUpdate, db: Session = Depends(get_db)):
    return customer_service.update_customer(db=db, customer_id=customer_id, payload=payload)


@router.delete("/{customer_id}", status_code=status.HTTP_200_OK)
def delete_customer(customer_id: int, db: Session = Depends(get_db)):
    return customer_service.delete_customer(db=db, customer_id=customer_id)
