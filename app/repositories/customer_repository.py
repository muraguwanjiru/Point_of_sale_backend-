from models.customer_model import Customer
from sqlalchemy.orm import Session

class CustomerRepository:
    def __init__(self):
        self.model = Customer

    def get(self, db: Session, id: int):
        return db.get(self.model, id)    

    def get_all(self, db: Session):
        return db.query(self.model).all()

    def create(self, db: Session, data: dict):
        db_obj = self.model(**data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, db_obj: Customer, update_data: dict):
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, db_obj: Customer):
        db.delete(db_obj)
        db.commit()
