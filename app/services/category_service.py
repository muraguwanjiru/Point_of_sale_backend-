from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from repositories.category_repository import CategoryRepository
from schemas.category_schema import CategoryCreate, CategoryUpdate

class CategoryService:
    def __init__(self):
        self.repository = CategoryRepository()

    def get_category(self, db: Session, category_id: int):
        category = self.repository.get(db, category_id)
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Category with ID {category_id} not found"
            )
        return category

    def get_all_categories(self, db: Session):
        return self.repository.get_all(db)

    def create_category(self, db: Session, payload: CategoryCreate):
        category_data = payload.model_dump()
        
        existing_category = db.query(self.repository.model).filter(
            self.repository.model.name == category_data["name"]
        ).first()
        
        if existing_category:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Category name already exists"
            )
            
        return self.repository.create(db, category_data)

    def update_category(self, db: Session, category_id: int, payload: CategoryUpdate):
        db_obj = self.get_category(db, category_id)
        update_data = payload.model_dump(exclude_unset=True)
        
        if "name" in update_data:
            existing_category = db.query(self.repository.model).filter(
                self.repository.model.name == update_data["name"],
                self.repository.model.category_id != category_id
            ).first()
            if existing_category:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Category name is already taken by another category"
                )
                
        return self.repository.update(db, db_obj, update_data)

    def delete_category(self, db: Session, category_id: int):
        db_obj = self.get_category(db, category_id)
        self.repository.delete(db, db_obj)
        return {"detail": "Category successfully deleted"}
