from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from dependencies import get_current_user
from repositories.supplier_repository import SupplierRepository
from schemas.supplier_schema import SupplierCreate, SupplierResponse  

router = APIRouter(prefix="/suppliers", tags=["Suppliers"],dependencies=[Depends(get_current_user)])

supplier_repo = SupplierRepository()

@router.post("/", response_model=SupplierResponse, status_code=status.HTTP_201_CREATED)
def create_supplier(payload: SupplierCreate, db: Session = Depends(get_db)):
    supplier_data = payload.model_dump()
    return supplier_repo.create(db=db, data=supplier_data)

@router.get("/", response_model=List[SupplierResponse])
def read_all_suppliers(db: Session = Depends(get_db)):
    return supplier_repo.get_all(db=db)

@router.get("/{supplier_id}", response_model=SupplierResponse)
def read_supplier(supplier_id: int, db: Session = Depends(get_db)):
    supplier = supplier_repo.get(db=db, id=supplier_id)
    if not supplier:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Supplier with ID {supplier_id} not found"
        )
    return supplier

@router.delete("/{supplier_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_supplier(supplier_id: int, db: Session = Depends(get_db)):
    supplier_obj = supplier_repo.get(db=db, id=supplier_id)
    if not supplier_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Supplier with ID {supplier_id} not found"
        )
    
    supplier_repo.delete(db=db, db_obj=supplier_obj)
    return None
