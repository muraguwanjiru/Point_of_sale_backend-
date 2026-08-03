from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from repositories.supplier_repository import SupplierRepository
from schemas.supplier_schema import SupplierCreate

class SupplierService:
    def __init__(self):
        self.supplier_repo = SupplierRepository()

    def create_supplier(self, db: Session, payload: SupplierCreate):
        supplier_data = payload.model_dump()
        return self.supplier_repo.create(db=db, data=supplier_data)

    def get_all_suppliers(self, db: Session):
        return self.supplier_repo.get_all(db=db)

    def get_supplier_by_id(self, db: Session, supplier_id: int):
        return self.supplier_repo.get(db=db, id=supplier_id)

    def delete_supplier_by_id(self, db: Session, supplier_id: int):
        supplier_obj = self.supplier_repo.get(db=db, id=supplier_id)
        if not supplier_obj:
            return None
        self.supplier_repo.delete(db=db, db_obj=supplier_obj)
        return supplier_obj
