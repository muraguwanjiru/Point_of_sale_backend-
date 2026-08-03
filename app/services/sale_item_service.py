from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from repositories.sale_item_repository import SaleItemRepository
from schemas.sale_item_schema import SaleItemCreate

class SaleItemService:
    def __init__(self):
        self.sale_item_repo = SaleItemRepository()

    def create_sale_item(self, db: Session, payload: SaleItemCreate):
        sale_item_data = payload.model_dump()
        return self.sale_item_repo.create(db=db, data=sale_item_data)

    def get_all_sale_items(self, db: Session):
        return self.sale_item_repo.get_all(db=db)

    def get_sale_item_by_id(self, db: Session, sale_item_id: int):
        return self.sale_item_repo.get(db=db, id=sale_item_id)

    def get_items_by_sale_id(self, db: Session, sale_id: int):
        return self.sale_item_repo.get_by_sale_id(db=db, sale_id=sale_id)

    def delete_sale_item_by_id(self, db: Session, sale_item_id: int):
        sale_item_obj = self.sale_item_repo.get(db=db, id=sale_item_id)
        if not sale_item_obj:
            return None
        self.sale_item_repo.delete(db=db, db_obj=sale_item_obj)
        return sale_item_obj
