from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from dependencies import get_current_user
from services.category_service import CategoryService
from schemas.category_schema import CategoryCreate, CategoryUpdate, CategoryResponse

router = APIRouter(
    prefix="/categories",
    tags=["Categories"],dependencies=[Depends(get_current_user)]
)

category_service = CategoryService()


@router.post("/", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
def create_category(payload: CategoryCreate, db: Session = Depends(get_db)):
    return category_service.create_category(db=db, payload=payload)


@router.get("/", response_model=List[CategoryResponse])
def read_all_categories(db: Session = Depends(get_db)):
    return category_service.get_all_categories(db=db)


@router.get("/{category_id}", response_model=CategoryResponse)
def read_category(category_id: int, db: Session = Depends(get_db)):
    return category_service.get_category(db=db, category_id=category_id)


@router.put("/{category_id}", response_model=CategoryResponse)
def update_category(category_id: int, payload: CategoryUpdate, db: Session = Depends(get_db)):
    return category_service.update_category(db=db, category_id=category_id, payload=payload)


@router.delete("/{category_id}", status_code=status.HTTP_200_OK)
def delete_category(category_id: int, db: Session = Depends(get_db)):
    return category_service.delete_category(db=db, category_id=category_id)
