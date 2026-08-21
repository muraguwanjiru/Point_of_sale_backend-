from models.user_model import User
from sqlalchemy import select
from sqlalchemy.orm import Session

class UserRepository:
    def __init__(self):
        self.model = User

   
    def get_by_id(self, db: Session, id: int):
        return db.get(self.model, id)    

  
    def get_by_username(self, db: Session, username: str):
        statement = select(self.model).filter_by(username=username)
        return db.execute(statement).scalar_one_or_none()

   
    def get_by_username_legacy(self, db: Session, username: str):
        return db.query(self.model).filter_by(username=username).first()

    def get_all(self, db: Session):
        return db.query(self.model).all()

    def create(self, db: Session, data: dict):
        db_obj = self.model(**data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, db_obj: User, update_data: dict):
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, db_obj: User):
        db.delete(db_obj)
        db.commit()
