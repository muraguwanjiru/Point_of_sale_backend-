from models.product_model import Product
from sqlalchemy.orm import Session

class ProductRepository:
    def __init__(self):
        self.model=Product

    def get(self,db:Session, id:int):
        return db.get(Product,id)    

    def get_all(self,db:Session):
        products = db.query(Product).all()

    def create(self,db:Session,data:dict):
        product =Product(**data)
        db.add(product)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete (self, db:Session,db_obj:Product):
        db.delete(db_obj)
