from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from dependencies import get_current_user
from services.user_service import UserService

from repositories.user_repository import UserRepository
from schemas.user_schema import UserCreate, UserUpdate, UserResponse

router = APIRouter(
    prefix="/users",
    tags=["Users"],
    dependencies=[Depends(get_current_user)]
)

user_service = UserService()


@router.post("/", response_model=UserResponse)
def create_user(payload: UserCreate, db: Session = Depends(get_db)):
    return user_service.create_user(db=db, payload=payload)


@router.get("/", response_model=List[UserResponse])
def read_all_users(db: Session = Depends(get_db)):
    return user_service.get_all_users(db=db)


@router.get("/username/{username}", response_model=UserResponse)
def read_user_by_username(username: str, db: Session = Depends(get_db)):
    return user_service.get_user_by_username(db=db, username=username)


@router.get("/{user_id}", response_model=UserResponse)
def read_user(user_id: int, db: Session = Depends(get_db)):
    return user_service.get_user(db=db, user_id=user_id)


@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, payload: UserUpdate, db: Session = Depends(get_db)):
    return user_service.update_user(db=db, user_id=user_id, payload=payload)


@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    return user_service.delete_user(db=db, user_id=user_id)
