from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from repositories.user_repository import UserRepository
from schemas.user_schema import UserCreate, UserUpdate ,UserResponse, UserBase

class UserService:
    def __init__(self):
        self.repository = UserRepository()

    def get_user(self, db: Session, user_id: int):
        user = self.repository.get(db, user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with ID {user_id} not found"
            )
        return user

    def get_all_users(self, db: Session):
        return self.repository.get_all(db)

    def create_user(self, db: Session, payload: UserCreate):
        user_data = payload.model_dump()
        
        existing_user = db.query(self.repository.model).filter(
            self.repository.model.username == user_data["username"]
        ).first()
        
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username is already taken"
            )
            
        return self.repository.create(db, user_data)

    def update_user(self, db: Session, user_id: int, payload: UserUpdate):
        db_obj = self.get_user(db, user_id)
        update_data = payload.model_dump(exclude_unset=True)
        
        if "username" in update_data:
            existing_user = db.query(self.repository.model).filter(
                self.repository.model.username == update_data["username"],
                self.repository.model.user_id != user_id
            ).first()
            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Username is already taken by another account"
                )
                
        return self.repository.update(db, db_obj, update_data)

    def delete_user(self, db: Session, user_id: int):
        db_obj = self.get_user(db, user_id)
        self.repository.delete(db, db_obj)
        return {"detail": "User successfully deleted"}
