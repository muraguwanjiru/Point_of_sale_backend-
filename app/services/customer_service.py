from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from repositories.customer_repository import CustomerRepository
from schemas.customer_schema import CustomerCreate, CustomerUpdate,CustomerResponse,CustomerBase

class CustomerService:
    def __init__(self):
        self.repository = CustomerRepository()

    def get_customer(self, db: Session, customer_id: int):
        customer = self.repository.get(db, customer_id)
        if not customer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Customer with ID {customer_id} not found"
            )
        return customer

    def get_all_customers(self, db: Session):
        return self.repository.get_all(db)

    def create_customer(self, db: Session, payload: CustomerCreate):
        customer_data = payload.model_dump()
        
        if customer_data.get("email"):
            existing_customer = db.query(self.repository.model).filter(
                self.repository.model.email == customer_data["email"]
            ).first()
            if existing_customer:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="A customer with this email already exists"
                )
                
        return self.repository.create(db, customer_data)

    def update_customer(self, db: Session, customer_id: int, payload: CustomerUpdate):
        db_obj = self.get_customer(db, customer_id)
        update_data = payload.model_dump(exclude_unset=True)
        
        if "email" in update_data and update_data["email"]:
            existing_customer = db.query(self.repository.model).filter(
                self.repository.model.email == update_data["email"],
                self.repository.model.customer_id != customer_id
            ).first()
            if existing_customer:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="This email address is already in use by another customer"
                )
                
        return self.repository.update(db, db_obj, update_data)

    def delete_customer(self, db: Session, customer_id: int):
        db_obj = self.get_customer(db, customer_id)
        self.repository.delete(db, db_obj)
        return {"detail": "Customer successfully deleted"}
