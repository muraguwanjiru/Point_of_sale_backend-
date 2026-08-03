from typing import List, Optional
from sqlalchemy.orm import Session
from models.supplier_model import Supplier

class SupplierRepository:
    def __init__(self):
        pass

    def create(self, db: Session, data: dict) -> Supplier:
        supplier = Supplier(
            company_name=data.get("company_name"),
            phone=data.get("phone"),
            contact_name=data.get("contact_name")
        )
        db.add(supplier)
        db.commit()
        db.refresh(supplier)
        return supplier

    def get(self, db: Session, id: int) -> Optional[Supplier]:
        return db.query(Supplier).filter(Supplier.supplier_id == id).first()

    def get_all(self, db: Session) -> List[Supplier]:
        return db.query(Supplier).all()

    def delete(self, db: Session, db_obj: Supplier) -> bool:
        db.delete(db_obj)
        db.commit()
        return True
