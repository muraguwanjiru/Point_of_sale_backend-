from typing import List, Optional
from sqlalchemy.orm import Session
from models.sale_item_model import SaleItem

class SaleItemRepository:
    def __init__(self):
        pass

    def create(self, db: Session, data: dict) -> SaleItem:
        sale_item = SaleItem(
            sale_id=data.get("sale_id"),
            product_id=data.get("product_id"),
            quantity=data.get("quantity"),
            unit_price=data.get("unit_price")
        )
        db.add(sale_item)
        db.commit()
        db.refresh(sale_item)
        return sale_item

    def get(self, db: Session, id: int) -> Optional[SaleItem]:
        return db.query(SaleItem).filter(SaleItem.sale_item_id == id).first()

    def get_all(self, db: Session) -> List[SaleItem]:
        return db.query(SaleItem).all()

    def get_by_sale_id(self, db: Session, sale_id: int) -> List[SaleItem]:
        return db.query(SaleItem).filter(SaleItem.sale_id == sale_id).all()

    def delete(self, db: Session, db_obj: SaleItem) -> bool:
        db.delete(db_obj)
        db.commit()
        return True
