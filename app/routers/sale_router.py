from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from dependencies import get_current_user
from repositories.sale_repository import SalesRepository
from schemas.sale_schema import SaleCreate, SaleResponse  


router = APIRouter(prefix="/sales",tags=["Sales",],dependencies=[Depends(get_current_user)])



sales_repo = SalesRepository()


@router.post("/", response_model=SaleResponse, status_code=status.HTTP_201_CREATED)
def create_sale(payload: SaleCreate, db: Session = Depends(get_db)):
    

    sale_data = payload.model_dump()
    return sales_repo.create(db=db, data=sale_data)


@router.get("/", response_model=List[SaleResponse])
def read_all_sales(db: Session = Depends(get_db)):
    """Fetches every sale record available."""
    return sales_repo.get_all(db=db)


@router.get("/{sale_id}", response_model=SaleResponse)
def read_sale(sale_id: float, db: Session = Depends(get_db)):
    """Fetches a specific sale record by its primary key ID."""
    sale = sales_repo.get(db=db, id=sale_id)
    if not sale:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Sale with ID {sale_id} not found"
        )
    return sale


@router.delete("/{sale_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_sale(sale_id: float, db: Session = Depends(get_db)):
    
    sale_obj = sales_repo.get(db=db, id=sale_id)
    if not sale_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Sale with ID {sale_id} not found"
        )
    
   
    sales_repo.delete(db=db, db_obj=sale_obj)
    return None
