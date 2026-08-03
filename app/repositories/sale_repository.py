from models.sale_model import Sale  
from sqlalchemy.orm import Session

class SalesRepository:
    def __init__(self):
        self.model = Sale

    def get(self, db: Session, id: float):
       
        return db.get(self.model, id)    

    def get_all(self, db: Session):
        
        return db.query(self.model).all()

    def create(self, db: Session, data: dict):
        
        db_obj = self.model(**data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, db_obj: Sale):
        
        db.delete(db_obj)
        db.commit()
