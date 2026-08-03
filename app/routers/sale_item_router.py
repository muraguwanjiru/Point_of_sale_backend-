from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from repositories.sale_item_repository import SaleItemRepository
from schemas.sale_item_schema import SaleItemCreate, SaleItemResponse  

router = APIRouter(prefix="/sale-items", tags=["Sale Items"])

sale_item_repo = SaleItemRepository()

@router.post("/", response_model=SaleItemResponse, status_code=status.HTTP_201_CREATED)
def create_sale_item(payload: SaleItemCreate, db: Session = Depends(get_db)):
    sale_item_data = payload.model_dump()
    return sale_item_repo.create(db=db, data=sale_item_data)

@router.get("/", response_model=List[SaleItemResponse])
def read_all_sale_items(db: Session = Depends(get_db)):
    return sale_item_repo.get_all(db=db)

@router.get("/{sale_item_id}", response_model=SaleItemResponse)
def read_sale_item(sale_item_id: int, db: Session = Depends(get_db)):
    sale_item = sale_item_repo.get(db=db, id=sale_item_id)
    if not sale_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Sale item with ID {sale_item_id} not found"
        )
    return sale_item

@router.get("/sale/{sale_id}", response_model=List[SaleItemResponse])
def read_sale_items_by_sale(sale_id: int, db: Session = Depends(get_db)):
    return sale_item_repo.get_by_sale_id(db=db, sale_id=sale_id)

@router.delete("/{sale_item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_sale_item(sale_item_id: int, db: Session = Depends(get_db)):
    sale_item_obj = sale_item_repo.get(db=db, id=sale_item_id)
    if not sale_item_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Sale item with ID {sale_item_id} not found"
        )
    
    sale_item_repo.delete(db=db, db_obj=sale_item_obj)
    return None
